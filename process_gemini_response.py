import json
import re

def process_gemini_response(gemini_response):
    if gemini_response is None:
        return {}

    categorized_data = {}

    categorized_text = gemini_response['candidates'][0]['content']['parts'][0]['text']

    # Use regex to match file name and categories
    pattern = r'(.+?):\s*(.+)'
    matches = re.findall(pattern, categorized_text)

    for file_name, category in matches:
        file_name = file_name.strip().replace("**", "").replace("*", "")
        category = category.strip().replace("**", "")
        categorized_data[file_name] = category

    return categorized_data
