from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import sqlite3
import io
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation

# Authenticate with Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  
drive = GoogleDrive(gauth)

# Connect to the database
db_path = "file_info.db"  # Change this to your actual database path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch a file ID from the database
cursor.execute("SELECT file_id, file_name, mime_type FROM files WHERE mime_type IN ('text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.presentationml.presentation')")
file_data = cursor.fetchone()

if file_data:
    file_id, file_name, mime_type = file_data
    print(f"Fetching content for: {file_name} ({mime_type})")

    # Get the file from Google Drive
    file = drive.CreateFile({'id': file_id})
    file_content = io.BytesIO()
    file.GetContentFile(file_name)

    # Read and print content based on file type
    if mime_type == "text/plain":
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()
    
    elif mime_type == "application/pdf":
        with open(file_name, "rb") as f:
            reader = PdfReader(f)
            content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file_name)
        content = "\n".join([para.text for para in doc.paragraphs])

    elif mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        prs = Presentation(file_name)
        content = "\n".join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])

    else:
        content = "Unsupported file type."

    print("\nFile Content:\n", content)

else:
    print("No readable files found in the database.")

# Close the database connection
conn.close()
