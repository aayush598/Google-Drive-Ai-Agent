import os
import json
import sqlite3
import re
import requests
from dotenv import load_dotenv
from controllers.fetch_content import fetch_all_file_contents
from services.auth import drive

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


def fetch_gemini_rename(file_name, file_content, api_key):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    file_base, file_extension = os.path.splitext(file_name)
    file_extension = file_extension.lstrip('.')
    
    prompt = f"""
    Based on the content of the following file, suggest a concise and meaningful file name (max 2 words).
    Use underscores instead of spaces, and retain the original file format. File name is provided with the file type
    for example file test.pdf here .pdf is the extension.
    Provide results in valid JSON format: {{"old_name": "<old_filename>", "new_name": "<new_filename>"}}.
    File: {file_name}
    Content: {file_content[:500]}...
    """
    
    request_body = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=request_body)
        response.raise_for_status()
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)
        
        rename_data = json.loads(result_text)
        new_name = rename_data["new_name"].replace(" ", "_")
        rename_data["new_name"] = f"{new_name}.{file_extension}"
        
        return rename_data
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        return None

def rename_file(drive, file_id, new_name):
    file = drive.CreateFile({'id': file_id})
    file.FetchMetadata()
    file['title'] = new_name
    file.Upload()
    print(f"Renamed file to: {new_name}")

def rename_files_endpoint():
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
    return renamed_files