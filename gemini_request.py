import requests
import json

def fetch_gemini_response(file_names, api_key):
    """
    Fetches categorization information from the Gemini API.

    Args:
    file_names (list): List of file names to categorize.
    api_key (str): Gemini API key for authentication.

    Returns:
    dict: Categorized file names and their corresponding categories.
    """
    gemini_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=' + api_key

    # Prepare the contents for the Gemini API request
    contents = []
    for file_name in file_names:
        content = {
            "role": "user",  # Specifying the role
            "parts": [{
                "text": f"""
                    Please categorize the following files into specific categories based on their content, type, or purpose. 
                    For each file, provide a category name. If the file can belong to multiple categories, list all relevant categories separated by commas. 
                    If no suitable category is found, label it as 'Uncategorized'. 
                    Be specific and clear with your categorization. 

                    Here are the files:
                    {', '.join([file.strip() for file in file_names])}

                    For each file, please follow this format:
                    - [File Name]: [Category 1], [Category 2], ... (if applicable)
                    """}]
        }
        contents.append(content)

    # Prepare the request data
    data = {'contents': contents}

    # Make the POST request to the Gemini API
    response = requests.post(
        gemini_url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)
    )

    # Return the response as JSON if successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
