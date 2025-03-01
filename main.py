import streamlit as st
from controllers.categorize import categorize_files
from controllers.fetch_content import fetch_all_file_contents
from controllers.fetch_files import fetch_all_file_names
from controllers.search import search_files_by_category
from controllers.move_file import move_selected_files, fetch_files_for_move
from controllers.rename_file import rename_files_endpoint
from controllers.permissions import fetch_all_permissions, view_permissions
from services.auth import drive
from services.logger import fetch_latest_logs
from services.pdf_generator import generate_pdf_from_analysis
import os

st.set_page_config(page_title="Google Drive AI Agent", layout="wide")
st.title("📂 Google Drive AI Agent - Streamlit Dashboard")

# Sidebar Navigation
menu = ["Categorize Files", "Fetch File Content", "Search Files", "Rename Files", "Manage Permissions", "Move Files", "View Logs"]
choice = st.sidebar.selectbox("Select an Action", menu)

# Categorize Files
if choice == "Categorize Files":
    if st.button("Categorize Files using Gemini AI"):
        result = categorize_files(drive)
        st.json(result)

# Fetch File Content
elif choice == "Fetch File Content":
    if st.button("Fetch Content from Drive"):
        files = fetch_all_file_contents()
        st.write(files)

# Search Files by Category
elif choice == "Search Files":
    category = st.text_input("Enter category to search:")
    if st.button("Search"):
        files = search_files_by_category(category)
        st.write(files)

# Rename Files
elif choice == "Rename Files":
    if st.button("Rename Files using AI"):
        response = rename_files_endpoint()
        st.write(response)

# Manage Permissions
elif choice == "Manage Permissions":
    if st.button("Fetch Permissions"):
        response = fetch_all_permissions(drive)
        st.json(response)

# Move Files
elif choice == "Move Files":
    files = fetch_files_for_move()
    st.write("Available files to move:", files)
    file_ids = st.multiselect("Select files to move:", [f["file_id"] for f in files])
    if st.button("Move Selected Files"):
        result = move_selected_files(file_ids)
        st.json(result)

# View Logs
elif choice == "View Logs":
    logs = fetch_latest_logs()
    st.write("Recent Logs:", logs)
    if st.button("Generate Log Analysis PDF"):
        analysis = generate_pdf_from_analysis(logs)
        st.success("PDF Report Generated!")
        st.download_button("Download Report", analysis, file_name="log_analysis.pdf")
