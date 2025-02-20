from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import sqlite3

# Authenticate and initialize Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens a browser for authentication
drive = GoogleDrive(gauth)

# Connect to the database
db_path = "file_info.db"  # Change to your actual database path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch files (excluding Google Docs, Sheets, etc.)
cursor.execute("SELECT file_id, file_name, mime_type FROM files WHERE mime_type NOT LIKE 'application/vnd.google-apps%'")
files = cursor.fetchall()

# Rename and update database
for file_id, old_name, mime_type in files:
    new_name = f"Renamed4_{old_name}"  # Update naming logic as needed

    try:
        # Fetch the existing file
        file = drive.CreateFile({'id': file_id})
        file.FetchMetadata()

        # Rename the file
        file['title'] = new_name
        file.Upload()

        print(f"Renamed: {old_name} → {new_name}")

        # Remove old file record from the database
        cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id,))

        # Update database with new file details
        cursor.execute(
            "INSERT INTO files (file_id, file_name, mime_type) VALUES (?, ?, ?)",
            (file_id, new_name, mime_type)
        )

        # Commit the database changes
        conn.commit()

    except Exception as e:
        print(f"Error renaming {old_name}: {e}")

# Close the database connection
conn.close()
