from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import sqlite3
import io
import pdfplumber  # Better PDF text extraction
from docx import Document
from pptx import Presentation

def authenticate_drive():
    """Authenticate with Google Drive and return a drive instance."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  
    return GoogleDrive(gauth)

def fetch_file_content():
    """Fetch all readable files from the database and extract their content."""
    db_path = "file_info.db"  # Change this to your actual database path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT file_id, file_name, mime_type FROM files 
        WHERE mime_type IN (
            'text/plain', 
            'application/pdf', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    """)

    files_data = cursor.fetchall()
    conn.close()
    
    if not files_data:
        return None, "No readable files found in the database."

    drive = authenticate_drive()
    all_files_content = []

    for file_id, file_name, mime_type in files_data:
        # Download file from Google Drive
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(file_name)

        # Extract content based on file type
        if mime_type == "text/plain":
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()
        elif mime_type == "application/pdf":
            with pdfplumber.open(file_name) as pdf:
                content = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file_name)
            content = "\n".join([para.text for para in doc.paragraphs])
        elif mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            prs = Presentation(file_name)
            content = "\n".join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])
        else:
            content = "Unsupported file type."

        all_files_content.append(f"File: {file_name}\n\n{content}\n\n{'-'*80}\n")

    return "Multiple Files", "\n".join(all_files_content)
