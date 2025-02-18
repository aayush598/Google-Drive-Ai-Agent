from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from googleapiclient.errors import HttpError
import sqlite3
def delete_files_and_folders(duplicates):
    """
    Deletes all duplicate files and folders from Google Drive based on the duplicate dictionary,
    and removes their entries from the database.

    Args:
    duplicates (dict): A dictionary containing duplicate file and folder names and their occurrences.

    Returns:
    None
    """
    # Authenticate using PyDrive2
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentication
    drive = GoogleDrive(gauth)

    # Connect to the SQLite database
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()

    for name, count in duplicates.items():
        if count > 1:
            # Retrieve all file and folder IDs with this name
            cursor.execute("SELECT file_id, is_folder FROM files WHERE file_name = ?", (name,))
            file_info = cursor.fetchall()

            # Delete all duplicates except the first occurrence
            for i, (file_id, is_folder) in enumerate(file_info):
                if i > 0:  # Skip the first occurrence, delete the rest
                    try:
                        if is_folder:  # If it's a folder
                            file_to_delete = drive.CreateFile({'id': file_id})
                            file_to_delete.FetchMetadata()  # Check if the folder exists
                            file_to_delete.Delete()
                            print(f"Folder with ID {file_id} has been deleted successfully.")
                        else:  # If it's a file
                            file_to_delete = drive.CreateFile({'id': file_id})
                            file_to_delete.FetchMetadata()  # Check if the file exists
                            file_to_delete.Delete()
                            print(f"File with ID {file_id} has been deleted successfully.")
                        
                        # Remove file/folder ID from the database
                        cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id,))
                        conn.commit()

                    except HttpError as e:
                        if e.resp.status == 404:
                            print(f"File or Folder with ID {file_id} not found. It might have already been deleted.")
                        else:
                            print(f"Failed to delete file/folder with ID {file_id}: {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

    conn.close()


def get_duplicates():
    """
    Retrieves duplicate files/folders from the database.

    Returns:
    dict: A dictionary containing duplicate file/folder names and their occurrences.
    """
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()

    # Retrieve duplicates based on file_name
    cursor.execute("""
        SELECT file_name, COUNT(*) 
        FROM files 
        GROUP BY file_name 
        HAVING COUNT(*) > 1
    """)
    duplicates = {name: count for name, count in cursor.fetchall()}

    conn.close()
    return duplicates