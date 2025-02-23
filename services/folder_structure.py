from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def create_folder(drive, folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive if it doesn't already exist.
    """
    query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    if parent_folder_id:
        query += f" and '{parent_folder_id}' in parents"
    
    folder_list = drive.ListFile({'q': query}).GetList()
    if folder_list:
        return folder_list[0]['id']
    
    folder_metadata = {
        'title': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        folder_metadata['parents'] = [{'id': parent_folder_id}]
    
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']

def setup_folder_structure(drive):
    """
    Define an optimized folder structure and create necessary folders in Google Drive.
    """
    folder_names = ["Documents", "Images", "Videos", "Projects", "Archives", "Work", "Personal"]
    folder_ids = {}
    
    for folder in folder_names:
        folder_id = create_folder(drive, folder)
        folder_ids[folder] = folder_id
        print(f"Folder '{folder}' is ready with ID {folder_id}")
    
    return folder_ids