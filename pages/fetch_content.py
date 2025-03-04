import streamlit as st
from controllers.fetch_content import fetch_all_file_contents
from services.logger import log_api_request

st.set_page_config(page_title="Fetch File Content", layout="wide")
st.title("📂 Fetch File Content")

if st.button("Fetch Content from Drive"):
    files = fetch_all_file_contents()
    log_api_request(
        endpoint="/fetch-files",
        request_method="GET",
        request_data={"action": "fetch_files"},
        response_data={"file_count": len(files)}
    )
    
    if files:
        st.subheader("📄 Extracted File Content")
        for file in files:
            with st.expander(f"📂 {file['file_name']}"):
                file_content = str(file['content'])  # Ensure content is a string
                if file_content.strip():  # Check if content is not empty
                    st.text_area("File Content", file_content, height=200)
                else:
                    st.warning("No content available.")
    else:
        st.warning("No readable files found in Google Drive.")
