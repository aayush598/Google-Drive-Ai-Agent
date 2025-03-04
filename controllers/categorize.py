import os
import sqlite3
from services.gemini_request import fetch_gemini_response
from services.process_gemini_response import process_gemini_response
from controllers.duplicate import find_duplicates
from controllers.deleteFile import delete_files_and_folders
from controllers.fetch_files import fetch_all_file_names
from dotenv import load_dotenv

load_dotenv()

def categorize_files(drive):
    """
    Fetches file names, categorizes them using Gemini AI, updates the database,
    and removes duplicates if found.
    """
    fetch_all_file_names(drive)  # Ensure file names are up to date

    # Read file names from the database
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_name FROM files")
    file_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not file_names:
        return {"message": "No files found to categorize."}

    api_key = os.getenv('GEMINI_API_KEY')
    gemini_response = fetch_gemini_response(file_names, api_key)
    categorized_data = process_gemini_response(gemini_response)

    duplicates = find_duplicates()
    if duplicates:
        delete_files_and_folders(duplicates,drive)

    return {
        'categorized_data': categorized_data,
        'duplicates': duplicates
    }
