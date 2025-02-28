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
    You are an **AI security auditor** specializing in **advanced sensitive data detection**.
    Analyze the provided file content and detect **hidden security risks**. 

    **🔍 Categories of Sensitive Information to Identify:**  
    1️⃣ **Personally Identifiable Information (PII)**  
       - Full names, addresses, emails, phone numbers, SSNs, passport numbers  
    2️⃣ **Financial & Payment Data**  
       - Credit card numbers, bank accounts, transaction details  
    3️⃣ **Authentication & Security Credentials**  
       - Passwords, API keys, OAuth tokens, SSH private keys, JWT tokens  
    4️⃣ **Confidential Business Data**  
       - Trade secrets, proprietary algorithms, internal emails, business reports  
    5️⃣ **Legal & Compliance Risks**  
       - NDAs, classified government documents, regulatory compliance risks  
    6️⃣ **Healthcare & Insurance Data (HIPAA-related)**  
       - Medical records, patient IDs, insurance numbers  
       
    If sensitive content is found, return:
    {{
        "file_name": "{file_name}",
        "sensitive": true,
        "description": "Detailed explanation of detected sensitive content.",
        "category": ["PII", "Financial", "Security", "Business", "Legal", "Healthcare"],
        "risk_level": "Low | Medium | High | Critical",
        "examples": ["Extracted examples of sensitive data from content"],
        "remediation": "Best practices to mitigate this risk."
    }}

    If no sensitive content is found, return:
    {{
        "file_name": "{file_name}",
        "sensitive": false,
        "description": "No sensitive information detected.",
        "risk_level": "None"
    }}

    **STRICT REQUIREMENTS**:
    - **ONLY output valid JSON** (no additional text or markdown).  
    - **Do NOT modify the file content**—only analyze it.  
    - **Detect obfuscated data (e.g., hidden passwords, masked card numbers)**.  
    - **Categorize risk as Low, Medium, High, or Critical** based on sensitivity.  
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
        print("Sensitive Data : ", sensitive_data)
        
        if sensitive_data.get("sensitive"):
            store_sensitive_data(
                sensitive_data["file_name"], 
                sensitive_data["description"], 
                sensitive_data.get("risk_level", "Unknown"),
                sensitive_data.get("category", []),
                sensitive_data.get("examples", []),
                sensitive_data.get("remediation", "No suggestions provided.")
            )

        return sensitive_data
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        return None


def store_sensitive_data(file_name, description, risk_level, category, examples, remediation):
    """Stores sensitive file details in the database, ensuring lists are stored as JSON strings."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()

    analysis_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert list fields to JSON strings
    category_json = json.dumps(category) if isinstance(category, list) else category
    examples_json = json.dumps(examples) if isinstance(examples, list) else examples
    remediation_json = json.dumps(remediation) if isinstance(remediation, list) else remediation

    cursor.execute('''
        INSERT INTO sensitive_files (file_name, analysis_time, description, risk_level, category, examples, remediation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (file_name, analysis_time, description, risk_level, category_json, examples_json, remediation_json))

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