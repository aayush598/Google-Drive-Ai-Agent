import sqlite3
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def authenticate_drive():
    """Authenticate with Google Drive and return a drive instance."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def delete_files_and_folders(duplicates):
    """Deletes duplicate files and folders from Google Drive and the database."""
    drive = authenticate_drive()
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()
    
    for file_name in duplicates:
        cursor.execute("SELECT file_id FROM files WHERE file_name = ?", (file_name,))
        file_ids = cursor.fetchall()
        
        for file_id in file_ids:
            try:
                file = drive.CreateFile({'id': file_id[0]})
                file.Delete()
                cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id[0],))
                conn.commit()
                print(f"Deleted: {file_name} ({file_id[0]})")
            except Exception as e:
                print(f"Error deleting {file_name}: {str(e)}")
    
    conn.close()

def get_duplicates():
    """Retrieves duplicate file entries from the database."""
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT file_name, COUNT(*) FROM files
        GROUP BY file_name
        HAVING COUNT(*) > 1
    """)
    
    duplicates = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return duplicates