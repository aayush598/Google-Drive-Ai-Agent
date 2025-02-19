from flask import Flask, render_template, request, jsonify
from gemini_request import fetch_gemini_response
from process_gemini_response import process_gemini_response
import os
from dotenv import load_dotenv
load_dotenv()

from fetchFiles import fetch_all_file_names
from duplicate import find_duplicates
from deleteFile import delete_files_and_folders, get_duplicates
from search import search_files_by_category

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categorize', methods=['POST'])
def categorize_files():
    # Fetch files from Google Drive only if not already done
    fetch_all_file_names()

    # Step 1: Read file names directly from 'file_names.txt'
    with open('file_names.txt', 'r') as file:
        file_names = file.readlines()[:]

    # Step 2: Fetch categorization response from Gemini API
    api_key = os.getenv('GEMINI_API_KEY')
    gemini_response = fetch_gemini_response(file_names, api_key)

    # Step 3: Process response and find duplicates
    categorized_data = process_gemini_response(gemini_response)
    duplicates = find_duplicates()

    duplicates2 = get_duplicates()
    if duplicates:
        # Delete duplicate files and folders from Google Drive and database
        delete_files_and_folders(duplicates)
    else:
        print("No duplicates found.")

    # Step 4: Return results as JSON
    return jsonify({
        'categorized_data': categorized_data,
        'duplicates': duplicates
    })

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    category_input = data.get('category', '')
    files = search_files_by_category(category_input)
    return jsonify({'files': files})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
