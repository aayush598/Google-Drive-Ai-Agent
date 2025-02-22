import requests
import json
import sqlite3
import os
from dotenv import load_dotenv
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from fetchContent import fetch_all_file_contents
import re

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Authenticate Google Drive
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

# Send a single file's content to Gemini API for renaming
def fetch_gemini_rename(file_name, file_content, api_key):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    
    prompt = f"""
    Based on the content of the following file, suggest a concise and meaningful file name (max 5 words).
    Use underscores instead of spaces, and retain the original file format.
    Provide results in valid JSON format: {{"old_name": "<old_filename>", "new_name": "<new_filename>"}}.
    File: {file_name}
    Content: {file_content[:500]}...
    """
    
    request_body = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=request_body)
        response.raise_for_status()
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        # Extract JSON from Markdown blocks if present
        json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        
        return json.loads(result_text)
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        return None

# Rename a file in Google Drive
def rename_file(drive, file_id, new_name):
    file = drive.CreateFile({'id': file_id})
    file.FetchMetadata()
    file['title'] = new_name
    file.Upload()
    print(f"Renamed file to: {new_name}")

if __name__ == "__main__":
    drive = authenticate_drive()
    
    file_data = fetch_all_file_contents()
    
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()
    
    renamed_files = []
    
    for file in file_data:
        old_name = file['file_name']
        content = file['content']
        rename_suggestion = fetch_gemini_rename(old_name, content, API_KEY)
        
        if rename_suggestion and "old_name" in rename_suggestion and "new_name" in rename_suggestion:
            new_name = rename_suggestion["new_name"]
            cursor.execute("SELECT file_id FROM files WHERE file_name = ?", (old_name,))
            result = cursor.fetchone()
            
            if result:
                file_id = result[0]
                rename_file(drive, file_id, new_name)
                cursor.execute("UPDATE files SET file_name = ? WHERE file_id = ?", (new_name, file_id))
                renamed_files.append({"old_name": old_name, "new_name": new_name})
                conn.commit()
    
    conn.close()
    
    print("Renaming completed:", json.dumps(renamed_files, indent=4))
