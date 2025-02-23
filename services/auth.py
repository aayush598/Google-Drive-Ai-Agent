from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def authenticate_drive():
    """Authenticate with Google Drive and return a drive instance."""
    gauth = GoogleAuth()
    
    # Try to load saved credentials
    gauth.LoadCredentialsFile("credentials.json")
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()  # First-time authentication
    elif gauth.access_token_expired:
        gauth.Refresh()  # Refresh expired token
    else:
        gauth.Authorize()  # Use existing credentials
    
    # Save credentials for future use
    gauth.SaveCredentialsFile("credentials.json")
    
    return GoogleDrive(gauth)

# Global drive instance
drive = authenticate_drive()
