from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from googleapiclient.errors import HttpError
import sqlite3

def delete_files(duplicates):
    """
    Deletes all duplicate files from Google Drive based on the duplicate dictionary,
    and removes their entries from the database.

    Args:
    duplicates (dict): A dictionary containing duplicate file names and their occurrences.

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

    for file_name, count in duplicates.items():
        if count > 1:
            # Retrieve all the file IDs with this name
            cursor.execute("SELECT file_id FROM files WHERE file_name = ?", (file_name,))
            file_ids = cursor.fetchall()

            # Delete all duplicates except the first occurrence
            for i, (file_id,) in enumerate(file_ids):
                if i > 0:  # Skip the first occurrence, delete the rest
                    try:
                        # Create a file object with the file ID
                        file_to_delete = drive.CreateFile({'id': file_id})

                        # Fetch metadata to check if the file exists
                        file_to_delete.FetchMetadata()

                        # Delete the file
                        file_to_delete.Delete()
                        print(f"File with ID {file_id} has been deleted successfully.")

                        # Remove file ID from the database
                        cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id,))
                        conn.commit()

                    except HttpError as e:
                        if e.resp.status == 404:
                            print(f"File with ID {file_id} not found. It might have already been deleted.")
                        else:
                            print(f"Failed to delete file with ID {file_id}: {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")
    
    conn.close()

