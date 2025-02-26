from flask import Blueprint, request, jsonify, render_template, send_file
from controllers.categorize import categorize_files
from controllers.fetch_content import fetch_all_file_contents
from controllers.fetch_files import fetch_all_file_names
from controllers.search import search_files_by_category
from controllers.move_file import move_selected_files, fetch_files_for_move
from controllers.rename_file import rename_files_endpoint
from controllers.permissions import fetch_all_permissions, view_permissions
from services.auth import drive
from services.logger import log_api_request, fetch_latest_logs, save_log_analysis
from services.gemini_request import fetch_gemini_log_analysis
from services.pdf_generator import generate_pdf_from_analysis
import sqlite3
import os

API_KEY = os.getenv("GEMINI_API_KEY")

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return render_template('index.html')

@api_bp.route('/categorize', methods=['POST'])
def categorize():
    result = categorize_files(drive)
    log_api_request("/categorize",result)
    return jsonify(result)

@api_bp.route('/fetch-content', methods=['GET'])
def fetch_content():
    files = fetch_all_file_contents()
    log_api_request("/fetch-content", {"files": files})
    return render_template('fetchContent.html', files=files)

@api_bp.route('/fetch-files', methods=['GET'])
def fetch_files():
    fetch_all_file_names(drive)
    response = {"message": "Files fetched successfully"}
    log_api_request("/fetch-files", response)
    return jsonify({"message": "Files fetched successfully"})

@api_bp.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    category_input = data.get('category', '')
    files = search_files_by_category(category_input)
    response = {'files': files}
    log_api_request("/search", response)
    return jsonify({'files': files})

# @api_bp.route('/move-files', methods=['GET'])
# def move_files():
#     result = move_files_to_documents()
#     log_api_request("/move-files", result)
#     return render_template('moveFiles.html', files_moved=result["files_moved"])

@api_bp.route('/rename-files', methods=['GET'])
def rename_files():
    response = rename_files_endpoint()
    log_api_request("/rename-files", response)
    return response

@api_bp.route('/fetch-permissions', methods=['GET'])
def fetch_permissions():
    response = fetch_all_permissions(drive)
    log_api_request("/fetch-permissions", response)
    return response

@api_bp.route('/view-permissions')
def view_permissions_page():
    response = view_permissions()
    log_api_request("/view-permissions", response)
    return response

@api_bp.route('/sensitive-files', methods=['GET'])
def view_sensitive_files():
    """Fetches and displays files marked as sensitive."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, analysis_time, sensitive_description FROM sensitive_files")
    sensitive_files = cursor.fetchall()
    conn.close()
    response = {"sensitive_files": sensitive_files}
    log_api_request("/sensitive-files", response)
    return render_template("sensitiveFiles.html", sensitive_files=sensitive_files)

@api_bp.route('/logs', methods=['GET'])
def view_logs():
    """Displays API logs from the database."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT endpoint, request_method, request_time, client_ip, request_data, response_data FROM api_logs ORDER BY request_time DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template("logs.html", logs=logs)

@api_bp.route('/analyze-logs', methods=['GET'])
def analyze_logs():
    """Fetch logs, analyze with Gemini, and generate a PDF report."""
    logs = fetch_latest_logs()
    analysis = fetch_gemini_log_analysis(logs, API_KEY)

    if analysis:
        filename = save_log_analysis(analysis)
        
        # Generate PDF
        pdf_path = generate_pdf_from_analysis(analysis)

        return render_template("logAnalysis.html", analysis=analysis, filename=filename, pdf_path=pdf_path)
    else:
        return render_template("logAnalysis.html", analysis=None, filename=None, pdf_path=None)

@api_bp.route('/download-report', methods=['GET'])
def download_report():
    """Serves the generated PDF report for download."""
    pdf_path = request.args.get("pdf_path")

    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "File not found", 404
    

@api_bp.route('/get-move-files', methods=['GET'])
def get_move_files():
    """Fetch files available for moving."""
    files = fetch_files_for_move()
    return render_template('confirmMove.html', files=files)

@api_bp.route('/move-selected-files', methods=['POST'])
def move_selected():
    """Move only the selected files."""
    data = request.get_json()
    selected_file_ids = data.get("selected_files", [])

    if not selected_file_ids:
        return jsonify({"message": "No files selected for moving."})

    result = move_selected_files(selected_file_ids)
    return jsonify(result)
