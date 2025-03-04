import streamlit as st
import json
from services.logger import fetch_latest_logs
from services.pdf_generator import generate_pdf_from_analysis

st.set_page_config(page_title="View Logs", layout="wide")
st.title("📂 View Logs")

logs = fetch_latest_logs()

if logs:
    st.subheader("📜 Recent Logs")
    for log in logs:
        with st.expander(f"📌 {log['endpoint']} - {log['time']}"):
            st.write(f"**Method:** {log['method']}")
            st.write(f"**Client IP:** {log['client_ip']}")
            st.write(f"**Request Data:** {log['request_data']}")
            
            try:
                parsed_response = json.loads(log['response_data'])
                st.json(parsed_response)
            except json.JSONDecodeError:
                st.write(f"**Response Data:** {log['response_data'][:200]}...")

if st.button("Generate Log Analysis PDF"):
    analysis = generate_pdf_from_analysis(logs)
    st.success("📄 PDF Report Generated!")
    st.download_button("📥 Download Report", analysis, file_name="log_analysis.pdf")
