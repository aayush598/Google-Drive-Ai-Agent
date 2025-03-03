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
import pandas as pd
import json

st.set_page_config(page_title="Google Drive AI Agent", layout="wide")
st.title("📂 Google Drive AI Agent - Streamlit Dashboard")

# Sidebar Navigation
menu = ["Categorize Files", "Fetch File Content", "Search Files", "Rename Files", "Manage Permissions", "Move Files", "View Logs"]
choice = st.sidebar.selectbox("Select an Action", menu)

# Categorize Files
if choice == "Categorize Files":
    if st.button("Categorize Files using Gemini AI"):
        result = categorize_files(drive)
        categorized_data = result.get("categorized_data", {})
        duplicates = result.get("duplicates", {})
        
        if categorized_data:
            st.subheader("📂 Categorized Files")
            data = [{"File Name": file, "Categories": categories} for file, categories in categorized_data.items()]
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.warning("No files found to categorize.")
        
        if duplicates:
            st.subheader("⚠️ Duplicate Files")
            dup_data = [{"File Name": file, "Count": count} for file, count in duplicates.items()]
            df_dup = pd.DataFrame(dup_data)
            st.dataframe(df_dup, hide_index=True, use_container_width=True)
        else:
            st.success("No duplicate files found.")

# Fetch File Content
elif choice == "Fetch File Content":
    if st.button("Fetch Content from Drive"):
        files = fetch_all_file_contents()
        
        if files:
            st.subheader("📄 Extracted File Content")
            for file in files:
                with st.expander(f"📂 {file['file_name']}"):
                    if file['content']:
                        st.text_area("File Content", file['content'], height=200)
                    else:
                        st.warning("No content available.")
        else:
            st.warning("No readable files found in Google Drive.")

# Search Files by Category
elif choice == "Search Files":
    category = st.text_input("🔍 Enter category to search:")
    if st.button("Search"):
        files = search_files_by_category(category)
        
        if files:
            st.subheader("📂 Search Results")
            st.write("Files matching the category:")
            st.markdown("\n".join([f"📄 {file}" for file in files]))
        else:
            st.warning("No files found for the given category.")

# Rename Files
elif choice == "Rename Files":
    if st.button("Rename Files using AI"):
        response = rename_files_endpoint()
        
        if response:
            st.subheader("📄 Renamed Files")
            rename_data = [{"Old Name": item["old_name"], "New Name": item["new_name"]} for item in response]
            df = pd.DataFrame(rename_data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.warning("No files were renamed.")

# Manage Permissions
elif choice == "Manage Permissions":
    if st.button("Fetch Permissions"):
        response = fetch_all_permissions(drive)
        
        if response:
            st.subheader("🔑 File Permissions")
            perm_data = [{"File ID": item["file_id"], "Email": item["email_address"], "Role": item["role"], "Type": item["type"]} for item in response]
            df = pd.DataFrame(perm_data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.warning("No permissions data found.")

# Move Files
elif choice == "Move Files":
    files = fetch_files_for_move()
    
    if files:
        st.subheader("🚀 Move Files")
        st.write("Available files to move:")
        file_options = {file["file_name"]: file["file_id"] for file in files}
        selected_files = st.multiselect("Select files to move:", list(file_options.keys()))
        
        if st.button("Move Selected Files"):
            selected_file_ids = [file_options[file] for file in selected_files]
            result = move_selected_files(selected_file_ids)
            st.success(result["message"])
            st.write("Files Moved:", result["files_moved"])
    else:
        st.warning("No files available for moving.")

# View Logs
elif choice == "View Logs":
    logs = fetch_latest_logs()
    
    if logs:
        st.subheader("📜 Recent Logs")
        for log in logs:
            with st.expander(f"📌 {log['endpoint']} - {log['time']}"):
                st.write(f"**Method:** {log['method']}")
                st.write(f"**Client IP:** {log['client_ip']}")
                st.write(f"**Request Data:** {log['request_data']}")
                
                response_data = log['response_data']
                try:
                    parsed_response = json.loads(response_data)
                    st.json(parsed_response)
                except json.JSONDecodeError:
                    st.write(f"**Response Data:** {response_data[:200]}...")
    else:
        st.warning("No logs available.")
    
    if st.button("Generate Log Analysis PDF"):
        analysis = generate_pdf_from_analysis(logs)
        st.success("📄 PDF Report Generated!")
        st.download_button("📥 Download Report", analysis, file_name="log_analysis.pdf")
