import streamlit as st
from controllers.move_file import move_selected_files, fetch_files_for_move

st.set_page_config(page_title="Move Files", layout="wide")
st.title("📂 Move Files")

files = fetch_files_for_move()
if files:
    st.subheader("🚀 Move Files")
    file_options = {file["file_name"]: file["file_id"] for file in files}
    selected_files = st.multiselect("Select files to move:", list(file_options.keys()))
    
    if st.button("Move Selected Files"):
        result = move_selected_files([file_options[file] for file in selected_files])
        st.success(result["message"])
        st.write("Files Moved:", result["files_moved"])
else:
    st.warning("No files available for moving.")
