import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Sensitive Files", layout="wide")
st.title("🔒 Sensitive Files Report")

# Fetch sensitive files from database
def fetch_sensitive_files():
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, analysis_time, description, risk_level, category, examples, remediation FROM sensitive_files")
    sensitive_files = cursor.fetchall()
    conn.close()
    return sensitive_files

sensitive_files = fetch_sensitive_files()

if sensitive_files:
    st.subheader("📜 Files Marked as Sensitive")
    df = pd.DataFrame(sensitive_files, columns=["File Name", "Analysis Time", "Description", "Risk Level", "Category", "Examples", "Remediation"])
    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.warning("No sensitive files detected.")
