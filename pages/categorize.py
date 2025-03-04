import streamlit as st
import pandas as pd
from controllers.categorize import categorize_files
from services.auth import drive
from services.logger import log_api_request

st.set_page_config(page_title="Categorize Files", layout="wide")
st.title("📂 Categorize Files")

if st.button("Categorize Files using Gemini AI"):
    result = categorize_files(drive)

    log_api_request(
        endpoint="/categorize-files",
        request_method="POST",
        request_data={"action": "categorize_files"},
        response_data=result
    )

    categorized_data = result.get("categorized_data", {})
    duplicates = result.get("duplicates", {})

    if categorized_data:
        st.subheader("📂 Categorized Files")
        df = pd.DataFrame([{"File Name": file, "Categories": categories} for file, categories in categorized_data.items()])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No files found to categorize.")

    if duplicates:
        st.subheader("⚠️ Duplicate Files")
        df_dup = pd.DataFrame([{"File Name": file, "Count": count} for file, count in duplicates.items()])
        st.dataframe(df_dup, hide_index=True, use_container_width=True)
    else:
        st.success("No duplicate files found.")
