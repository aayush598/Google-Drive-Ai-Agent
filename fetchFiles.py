import sqlite3
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from folderStructure import setup_folder_structure

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('file_info.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table to store file information with UNIQUE constraint on file_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT UNIQUE,
        file_name TEXT,
        mime_type TEXT,
        parent_folder TEXT,
        created_time TEXT,
        modified_time TEXT
    )
''')
conn.commit()

def fetch_all_file_names(output_file='file_names.txt'):
    """
    Authenticate with Google Drive using PyDrive2 and fetch all file details.
    Store the file details in an SQLite database.
    
    Args:
    output_file (str): The name of the output file where the file names will be stored. Default is 'file_names.txt'.
    
    Returns:
    None
    """
    # Authenticate using PyDrive2
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentication
    drive = GoogleDrive(gauth)

    folder_ids = setup_folder_structure(drive)

    # Fetch all files from Google Drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    # Open a file to write the file names
    with open(output_file, 'w') as file:
        for file_item in file_list:
            file_name = file_item['title']
            file_id = file_item['id']
            mime_type = file_item['mimeType']
            parent_folder = file_item['parents'][0]['id'] if 'parents' in file_item else 'No Parent'
            created_time = file_item['createdDate']
            modified_time = file_item['modifiedDate']

            # Check if file_id already exists in the database
            cursor.execute("SELECT file_id FROM files WHERE file_id = ?", (file_id,))
            existing_file = cursor.fetchone()

            if existing_file is None:  # Only insert if file_id is not already in the database
                cursor.execute('''
                    INSERT INTO files (file_id, file_name, mime_type, parent_folder, created_time, modified_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (file_id, file_name, mime_type, parent_folder, created_time, modified_time))
                conn.commit()
                print(f"Inserted: {file_name} ({file_id})")
            else:
                print(f"Skipped (duplicate): {file_name} ({file_id})")

            # Write the file name to the output file
            file.write(file_name + '\n')

    print(f"All file names and details have been saved to SQLite and '{output_file}'.")

# Example usage
fetch_all_file_names()
