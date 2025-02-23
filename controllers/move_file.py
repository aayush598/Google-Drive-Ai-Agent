import sqlite3
from services.auth import drive

def get_documents_folder_id(drive):
    """Get the folder ID of 'Documents' in Google Drive. If not found, create one."""
    query = "title = 'Documents' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    folder_list = drive.ListFile({'q': query}).GetList()
    
    if folder_list:
        return folder_list[0]['id']  # Return existing folder ID
    else:
        folder_metadata = {
            'title': 'Documents',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

def move_files_to_documents():
    """Move all PDF and PPT files inside the 'Documents' folder in Google Drive."""
    db_path = "file_info.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT file_id, file_name FROM files 
        WHERE mime_type IN (
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    """)
    
    files_data = cursor.fetchall()
    conn.close()
    
    if not files_data:
        return {"message": "No PDF or PPT files found in the database.", "files_moved": []}
    
    documents_folder_id = get_documents_folder_id(drive)
    
    moved_files = []
    
    for file_id, file_name in files_data:
        file = drive.CreateFile({'id': file_id})
        file['parents'] = [{'id': documents_folder_id}]
        file.Upload()
        moved_files.append(file_name)
    
    return {"message": f"Moved {len(moved_files)} files to Documents folder.", "files_moved": moved_files}
