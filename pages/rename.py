import streamlit as st
import pandas as pd
from controllers.rename_file import rename_files_endpoint
from services.logger import log_api_request

st.set_page_config(page_title="Rename Files", layout="wide")
st.title("📂 Rename Files")

if st.button("Rename Files using AI"):
    response = rename_files_endpoint()
    log_api_request(
        endpoint="/rename-files",
        request_method="POST",
        request_data={"action": "rename_files"},
        response_data={"renamed_files": response}
    )
    if response:
        st.subheader("📄 Renamed Files")
        df = pd.DataFrame([{"Old Name": item["old_name"], "New Name": item["new_name"]} for item in response])
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No files were renamed.")
