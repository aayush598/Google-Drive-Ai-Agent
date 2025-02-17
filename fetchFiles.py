from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def fetch_all_file_names(output_file='file_names.txt'):
    """
    Authenticate with Google Drive using PyDrive2 and fetch all file names.
    
    Args:
    output_file (str): The name of the output file where the file names will be stored. Default is 'file_names.txt'.
    
    Returns:
    None
    """
    # Authenticate using PyDrive2
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authentication
    drive = GoogleDrive(gauth)

    # Fetch all files from Google Drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    # Open a file to write the file names
    with open(output_file, 'w') as file:
        for file_item in file_list:
            file.write(file_item['title'] + '\n')

    print(f"All file names have been saved to '{output_file}'.")
