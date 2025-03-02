import sqlite3
from services.auth import drive
from services.logger import log_api_request

def get_documents_folder_id(drive):
    """Get the folder ID of 'Documents' in Google Drive. If not found, create one."""
    query = "title = 'Documents' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    folder_list = drive.ListFile({'q': query}).GetList()
    
    if folder_list:
        return folder_list[0]['id']
    else:
        folder_metadata = {'title': 'Documents', 'mimeType': 'application/vnd.google-apps.folder'}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

def fetch_files_for_move():
    """Fetch files available for moving and return data."""
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

    return [{"file_id": file_id, "file_name": file_name} for file_id, file_name in files_data]

def move_selected_files(file_ids):
    """Move selected files to the 'Documents' folder in Google Drive."""
    documents_folder_id = get_documents_folder_id(drive)
    moved_files = []

    for file_id in file_ids:
        file = drive.CreateFile({'id': file_id})
        file['parents'] = [{'id': documents_folder_id}]
        file.Upload()
        moved_files.append(file["title"])

    result = {"message": f"Moved {len(moved_files)} files to Documents folder.", "files_moved": moved_files}
    
    # Modify log function to work without Flask request context
    # log_api_request("/move-files", str(result))  

    return result
