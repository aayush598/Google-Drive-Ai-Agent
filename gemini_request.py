import requests
import json

def fetch_gemini_response(file_names, api_key):
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
            """}]
    }]

    data = {'contents': contents}

    try:
        response = requests.post(gemini_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
