from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import sqlite3

# Authenticate and create a PyDrive2 GoogleDrive instance
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens a browser for authentication
    return GoogleDrive(gauth)

# Connect to the database and fetch file details
def fetch_files_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, file_name, mime_type FROM files")
    files = cursor.fetchall()
    conn.close()
    return files

# Rename a file in Google Drive
def rename_file(drive, file_id, new_name):
    file = drive.CreateFile({'id': file_id})
    file.FetchMetadata()  # Fetch current metadata
    file['title'] = new_name  # Set new file name
    file.Upload()  # Apply changes
    print(f"Renamed file to: {new_name}")

if __name__ == "__main__":
    database_path = "file_info.db"  # Update with actual database path
    drive = authenticate_drive()
    
    files = fetch_files_from_db(database_path)
    for file_id, file_name, mime_type in files:
        if not mime_type.startswith("application/vnd.google-apps"):  # Skip Google Docs, Sheets, etc.
            new_name = "Renamed_" + file_name  # Modify naming logic as needed
            rename_file(drive, file_id, new_name)
