import streamlit as st
from controllers.search import search_files_by_category
from services.logger import log_api_request

st.set_page_config(page_title="Search Files", layout="wide")
st.title("📂 Search Files")

category = st.text_input("🔍 Enter category to search:")
if st.button("Search"):
    files = search_files_by_category(category)
    log_api_request(
        endpoint="/search-files",
        request_method="GET",
        request_data={"category": category},
        response_data={"results": files}
    )
    if files:
        st.subheader("📂 Search Results")
        st.markdown("\n".join([f"📄 {file}" for file in files]))
    else:
        st.warning("No files found for the given category.")