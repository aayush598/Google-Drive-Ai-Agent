from flask import Blueprint, request, jsonify, render_template
from controllers.categorize import categorize_files
from controllers.fetch_content import fetch_all_file_contents
from controllers.fetch_files import fetch_all_file_names
from controllers.search import search_files_by_category
from controllers.move_file import move_files_to_documents
from controllers.rename_file import rename_files_endpoint
from controllers.permissions import fetch_all_permissions, view_permissions
from services.auth import drive
import sqlite3

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return render_template('index.html')

@api_bp.route('/categorize', methods=['POST'])
def categorize():
    result = categorize_files(drive)
    print(f"Categorized result : {result}")
    return jsonify(result)

@api_bp.route('/fetch-content', methods=['GET'])
def fetch_content():
    files = fetch_all_file_contents()
    return render_template('fetchContent.html', files=files)

@api_bp.route('/fetch-files', methods=['GET'])
def fetch_files():
    fetch_all_file_names()
    return jsonify({"message": "Files fetched successfully"})

@api_bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    print(f"Data received: {data}")
    category_input = data.get('category', '')
    files = search_files_by_category(category_input)
    return jsonify({'files': files})

@api_bp.route('/move-files', methods=['GET'])
def move_files():
    result = move_files_to_documents()
    return render_template('moveFiles.html', files_moved=result["files_moved"])

@api_bp.route('/rename-files', methods=['GET'])
def rename_files():
    return rename_files_endpoint()

@api_bp.route('/fetch-permissions', methods=['GET'])
def fetch_permissions():
    return fetch_all_permissions(drive)

@api_bp.route('/view-permissions')
def view_permissions_page():
    return view_permissions()

@api_bp.route('/sensitive-files', methods=['GET'])
def view_sensitive_files():
    """Fetches and displays files marked as sensitive."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()

    cursor.execute("SELECT file_name, analysis_time, sensitive_description FROM sensitive_files")
    sensitive_files = cursor.fetchall()
    
    conn.close()
    return render_template("sensitiveFiles.html", sensitive_files=sensitive_files)