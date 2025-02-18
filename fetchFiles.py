import sqlite3
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from folderStructure import setup_folder_structure

# Connect to SQLite database
conn = sqlite3.connect('file_info.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT UNIQUE,
        file_name TEXT,
        mime_type TEXT,
        parent_folder TEXT,
        created_time TEXT,
        modified_time TEXT,
        is_folder INTEGER DEFAULT 0
    )
''')
conn.commit()

def fetch_all_file_names(output_file='file_names.txt'):
    # Authenticate with PyDrive2
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_ids = setup_folder_structure(drive)

    # Fetch files from Google Drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    file_ids = [file_item['id'] for file_item in file_list]
    cursor.execute("SELECT file_id FROM files WHERE file_id IN ({})".format(','.join('?' * len(file_ids))), file_ids)
    existing_files = {row[0] for row in cursor.fetchall()}

    # Open the output file to write file names
    with open(output_file, 'w') as file:
        for file_item in file_list:
            file_name = file_item['title']
            file_id = file_item['id']
            is_folder = 1 if file_item['mimeType'] == 'application/vnd.google-apps.folder' else 0

            if file_id not in existing_files:
                cursor.execute('''
                    INSERT INTO files (file_id, file_name, mime_type, parent_folder, created_time, modified_time, is_folder)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (file_id, file_name, file_item['mimeType'], file_item['parents'][0]['id'] if 'parents' in file_item else 'No Parent', file_item['createdDate'], file_item['modifiedDate'], is_folder))
                conn.commit()
                print(f"Inserted: {file_name} ({file_id})")
            file.write(file_name + '\n')

    print(f"All file names and details have been saved to SQLite and '{output_file}'.")
