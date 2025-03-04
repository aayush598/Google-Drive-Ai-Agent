import streamlit as st

st.set_page_config(page_title="Google Drive AI Agent", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select a feature:",
    ["Home", "Categorize Files", "Fetch File Content", "Search Files", "Rename Files", "Manage Permissions", "Move Files", "View Logs", "Sensitive Files", "Log Analysis"]
)

# Redirect to the selected page
if page == "Home":
    st.title("📂 Google Drive AI Agent - Streamlit Dashboard")
    st.write("Welcome to the AI-powered file management system!")
elif page == "Categorize Files":
    st.switch_page("pages/categorize.py")
elif page == "Fetch File Content":
    st.switch_page("pages/fetch_content.py")
elif page == "Search Files":
    st.switch_page("pages/search.py")
elif page == "Rename Files":
    st.switch_page("pages/rename.py")
elif page == "Manage Permissions":
    st.switch_page("pages/permissions.py")
elif page == "Move Files":
    st.switch_page("pages/move_files.py")
elif page == "View Logs":
    st.switch_page("pages/logs.py")
elif page == "Sensitive Files":
    st.switch_page("pages/sensitive_files.py")
elif page == "Log Analysis":
    st.switch_page("pages/log_analysis.py")