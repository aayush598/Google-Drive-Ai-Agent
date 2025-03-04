import streamlit as st
import pandas as pd
from controllers.permissions import fetch_all_permissions
from services.auth import drive

st.set_page_config(page_title="Manage Permissions", layout="wide")
st.title("📂 Manage Permissions")

if st.button("Fetch Permissions"):
    response = fetch_all_permissions(drive)
    if response:
        st.subheader("🔑 File Permissions")
        df = pd.DataFrame([{"File ID": item["file_id"], "Email": item["email_address"], "Role": item["role"], "Type": item["type"]} for item in response])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No permissions data found.")
