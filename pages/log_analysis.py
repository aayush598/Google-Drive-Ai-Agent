import streamlit as st
import json
import requests
import os
import datetime
from services.logger import fetch_latest_logs
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Log Analysis", layout="wide")
st.title("📊 Log Analysis & Insights")


API_KEY = os.getenv("GEMINI_API_KEY")

# Function to analyze logs with Gemini API
def fetch_gemini_log_analysis(logs, api_key):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'
    prompt = f"""
    Analyze the following API logs and generate meaningful insights:
    - Identify common API usage patterns.
    - Detect unusual activities or repeated errors.
    - Suggest optimizations or improvements.

    **Logs for Analysis (JSON Format):**
    {json.dumps(logs, indent=2)}

    **STRICT REQUIREMENTS:**  
    - Respond **ONLY** in valid JSON format.  
    - Do **NOT** include markdown formatting (```json).  
    - Do **NOT** add any extra text before or after the JSON response.  
    - The response **must be a valid JSON object** with the following structure:
    
    {{
        "summary": "A brief summary of the log insights.",
        "common_patterns": ["Pattern 1", "Pattern 2"],
        "anomalies_detected": ["Issue 1", "Issue 2"],
        "recommendations": ["Suggestion 1", "Suggestion 2"]
    }}

    **Important: Your response should be a JSON object, and nothing else.**
    """
    
    request_body = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=request_body)
        response.raise_for_status()
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(result_text)
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        st.error(f"Error: {e}")
        return None

# Fetch logs
logs = fetch_latest_logs()

if logs:

    if st.button("Analyze Logs with Gemini AI"):
        analysis = fetch_gemini_log_analysis(logs, API_KEY)
        if analysis:
            st.subheader("🔍 Insights from Log Analysis")
            st.write(f"**📌 Summary:** {analysis['summary']}")
            st.write(f"**📊 Common Patterns:** {', '.join(analysis['common_patterns'])}")
            st.write(f"**⚠️ Anomalies Detected:** {', '.join(analysis['anomalies_detected'])}")
            st.write(f"**✅ Recommendations:** {', '.join(analysis['recommendations'])}")

            # Generate PDF
            pdf_filename = f"log_analysis_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
else:
    st.warning("No logs available.")
