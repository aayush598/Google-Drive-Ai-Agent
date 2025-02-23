import sqlite3
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from services.folder_structure import setup_folder_structure

db_path = "file_info.db"

def fetch_all_file_names():
    """
    Fetches file details from Google Drive and stores them in the database.
    """
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    folder_ids = setup_folder_structure(drive)
    
    conn = sqlite3.connect(db_path)
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
            is_folder INTEGER DEFAULT 0,
            category TEXT
        )
    ''')
    conn.commit()
    
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    file_ids = [file_item['id'] for file_item in file_list]
    
    cursor.execute("SELECT file_id FROM files WHERE file_id IN ({})".format(','.join('?' * len(file_ids))), file_ids)
    existing_files = {row[0] for row in cursor.fetchall()}
    
    for file_item in file_list:
        file_id = file_item['id']
        file_name = file_item['title']
        is_folder = 1 if file_item['mimeType'] == 'application/vnd.google-apps.folder' else 0

        if file_id not in existing_files:
            cursor.execute('''
                INSERT INTO files (file_id, file_name, mime_type, parent_folder, created_time, modified_time, is_folder, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_id, file_name, file_item['mimeType'],
                file_item['parents'][0]['id'] if 'parents' in file_item else 'No Parent',
                file_item['createdDate'], file_item['modifiedDate'], is_folder, None
            ))
            conn.commit()
            print(f"Inserted: {file_name} ({file_id})")

    conn.close()
    print("All file names and details have been saved to SQLite.")
