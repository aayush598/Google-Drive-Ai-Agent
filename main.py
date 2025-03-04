import streamlit as st

st.set_page_config(page_title="Google Drive AI Agent", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select a feature:",
    ["Home", "Categorize Files",  "Search Files", "Rename Files", "Manage Permissions", "Move Files", "View Logs", "Sensitive Files", "Log Analysis"]
)   

# Redirect to the selected page
if page == "Home":
    st.title("📂 Google Drive AI Agent - Streamlit Dashboard")
    st.write(
        """
        Welcome to the **Google Drive AI Agent**! This tool helps you **categorize, rename, search, manage permissions, 
        and analyze files** in Google Drive using AI-powered automation.
        
        ### 🚀 **Features:**
        - **Categorize Files**: Uses AI to categorize files based on their content.
        - **Search Files**: Quickly find files by category.
        - **Rename Files**: Automatically rename files based on their content.
        - **Manage Permissions**: View and update file access permissions.
        - **Move Files**: Move files to appropriate folders in Google Drive.
        - **View Logs**: Track actions performed on files.
        - **Sensitive Files Detection**: Identify sensitive data in your Drive.
        - **Log Analysis**: Get AI-generated insights from recent activity logs.
        
        ### 📌 **How to Use:**
        1️⃣ Use the **Sidebar** to navigate between features.  
        2️⃣ Click on a function (e.g., "Categorize Files") and follow the on-screen instructions.  
        3️⃣ AI-powered automation will handle tasks like categorization, renaming, and analysis.  
        4️⃣ View results in a **user-friendly format**.  

        ✅ **Start organizing your Google Drive efficiently!**  
        """
    )
elif page == "Categorize Files":
    st.switch_page("pages/categorize.py")
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