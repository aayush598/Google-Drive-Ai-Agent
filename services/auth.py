from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def authenticate_drive():
    """Authenticate with Google Drive and return a drive instance."""
    gauth = GoogleAuth()

    # Ensure OAuth is set to offline mode
    gauth.settings["get_refresh_token"] = True  # Request refresh token

    # Try to load saved credentials
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()  # First-time authentication (generates refresh_token)
    elif gauth.access_token_expired:
        try:
            gauth.Refresh()  # Attempt to refresh token
        except:
            print("Token refresh failed. Re-authenticating...")
            gauth.LocalWebserverAuth()  # Re-authenticate if refresh fails
    else:
        gauth.Authorize()  # Use existing credentials

    # Save credentials for future use
    gauth.SaveCredentialsFile("credentials.json")

    return GoogleDrive(gauth)

# Global drive instance
drive = authenticate_drive()
