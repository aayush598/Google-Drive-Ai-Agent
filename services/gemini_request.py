import requests
import json
import datetime
import sqlite3
import re

def fetch_gemini_response(file_names, api_key):
    """
    Sends a request to the Gemini API to categorize file names.
    """
    gemini_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}'
    
    contents = [{
        "role": "user",
        "parts": [{
            "text": f"""
                Please categorize the following files into specific categories based on their content, type, or purpose. 
                For each file, provide a category name. If the file can belong to multiple categories, list all relevant categories separated by commas. 
                If no suitable category is found, label it as 'Uncategorized'. 
                Be specific and clear with your categorization. 
                
                Here are the files:
                {', '.join(file_names)}

                For each file, please follow this format:
                - [File Name]: [Category 1], [Category 2], ... (if applicable)
            """
        }]
    }]
    
    data = {'contents': contents}
    
    try:
        response = requests.post(gemini_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def fetch_gemini_sensitive_analysis(file_name, file_content, api_key):
    """Sends a request to Gemini API to analyze sensitive content in files."""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    
    prompt = f"""
    Analyze the content of this file and detect any sensitive data such as:
    - Personally Identifiable Information (PII) (e.g., names, addresses, phone numbers, emails, SSN)
    - Financial details (e.g., bank account numbers, credit card details)
    - Confidential business information (e.g., proprietary data, internal communications)

    If sensitive content is found, return:
    {{
        "file_name": "{file_name}",
        "sensitive": true,
        "description": "Brief explanation of detected sensitive content."
    }}

    If no sensitive content is found, return:
    {{
        "file_name": "{file_name}",
        "sensitive": false,
        "description": "No sensitive information detected."
    }}

    **STRICT REQUIREMENTS**:
    - Respond **ONLY** with valid JSON. 
    - Do **not** add any extra text, explanations, or formatting outside JSON.

    File Content (First 1000 characters for analysis):
    \"\"\"{file_content[:1000]}\"\"\"
    """

    request_body = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=request_body)
        response.raise_for_status()
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        # Ensure only valid JSON is extracted
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(0)

        sensitive_data = json.loads(result_text)
        
        if sensitive_data.get("sensitive"):
            store_sensitive_data(sensitive_data["file_name"], sensitive_data["description"])

        return sensitive_data
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        return None


def store_sensitive_data(file_name, description):
    """Stores sensitive file details in the database."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()

    analysis_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO sensitive_files (file_name, analysis_time, sensitive_description)
        VALUES (?, ?, ?)
    ''', (file_name, analysis_time, description))

    conn.commit()
    conn.close()

def fetch_gemini_log_analysis(logs, api_key):
    """Sends the latest logs to Gemini API for analytics and ensures pure JSON output."""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'

    prompt = f"""
    Analyze the following API logs and generate meaningful insights:
    - Identify common API usage patterns.
    - Detect unusual activities or repeated errors.
    - Suggest optimizations or improvements.

    **Logs for Analysis (JSON Format):**
    {json.dumps(logs, indent=2)}

    **STRICT REQUIREMENTS:**  
    - Respond **ONLY** in valid JSON format.  
    - Do **NOT** include markdown formatting (```json).  
    - Do **NOT** add any extra text before or after the JSON response.  
    - The response **must be a valid JSON object** with the following structure:
    
    {{
        "summary": "A brief summary of the log insights.",
        "common_patterns": ["Pattern 1", "Pattern 2"],
        "anomalies_detected": ["Issue 1", "Issue 2"],
        "recommendations": ["Suggestion 1", "Suggestion 2"]
    }}

    **Important: Your response should be a JSON object, and nothing else.**
    """

    request_body = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=request_body)
        response.raise_for_status()
        
        # Extract text response
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        
        # Remove unwanted markdown formatting if present
        result_text = re.sub(r"```json\n|\n```", "", result_text).strip()

        # Convert to valid JSON
        json_data = json.loads(result_text)
        return json_data

    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        return None