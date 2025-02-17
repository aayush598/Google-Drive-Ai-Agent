import json

def process_gemini_response(gemini_response):
    """
    Processes the response from Gemini and categorizes the files.
    
    Args:
    gemini_response (dict): The response JSON from the Gemini API.

    Returns:
    dict: A dictionary of file names and their categorized categories.
    """
    if gemini_response is None:
        return {}

    categorized_data = {}
    
    # Extract the categorized text from the Gemini response
    categorized_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
    
    # Split the response to extract filenames and their categories
    lines = categorized_text.split("\n")
    for line in lines:
        if line.strip() and ":" in line:  # Ensure there is no empty line and a valid ':' exists
            parts = line.split(":")
            if len(parts) == 2:
                file_name = parts[0].strip().replace("**", "")  # Remove any Markdown formatting
                file_name = file_name.replace("*", "")
                category = parts[1].strip().replace("**", "")
                categorized_data[file_name] = category
    
    return categorized_data
