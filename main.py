from flask import Flask, render_template, request, redirect, url_for, jsonify
from gemini_request import fetch_gemini_response
from process_gemini_response import process_gemini_response
import os
from dotenv import load_dotenv
load_dotenv()

from fetchFiles import fetch_all_file_names
from duplicate import find_duplicates
from deleteFile import delete_files  # Import the delete_files function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categorize', methods=['POST'])
def categorize_files():
    # Fetch files from Google Drive
    fetch_all_file_names()

    # Step 1: Read the first 20 file names from 'file_names.txt'
    with open('file_names.txt', 'r') as file:
        file_names = file.readlines()

    # Get the first 20 file names
    first_20_files = file_names[:]

    # Step 2: Fetch response from Gemini API using the file names
    api_key = os.getenv('GEMINI_API_KEY')
    gemini_response = fetch_gemini_response(first_20_files, api_key)

    # Step 3: Process the response from Gemini
    categorized_data = process_gemini_response(gemini_response)

    duplicates = find_duplicates(file_names=first_20_files)

    # delete_files(duplicates)  # Call the delete_files function

    # Step 4: Return the categorized data as JSON
    return jsonify({
        'categorized_data': categorized_data,
        'duplicates': duplicates
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
