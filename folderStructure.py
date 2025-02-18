from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def create_folder(drive, folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive.

    Args:
        drive: GoogleDrive instance.
        folder_name (str): Name of the folder to be created.
        parent_folder_id (str, optional): Parent folder ID if creating inside another folder.

    Returns:
        str: The created folder's ID.
    """
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

    Args:
        drive: GoogleDrive instance.

    Returns:
        dict: Dictionary mapping folder names to their respective IDs.
    """
    folder_names = ["Documents", "Images", "Videos", "Projects", "Archives", "Work", "Personal"]
    folder_ids = {}

    for folder in folder_names:
        folder_id = create_folder(drive, folder)
        folder_ids[folder] = folder_id
        print(f"Created folder: {folder} with ID {folder_id}")

    return folder_ids
