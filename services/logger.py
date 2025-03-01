import sqlite3
import datetime
import json
from flask import request

def log_api_request(endpoint, response_data):
    """Logs API requests and responses in the database."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()

    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_method = request.method
    client_ip = request.remote_addr
    request_data = json.dumps(request.get_json()) if request.is_json else "No JSON Data"
    response_data = json.dumps(response_data) if isinstance(response_data, dict) else str(response_data)

    cursor.execute('''
        INSERT INTO api_logs (endpoint, request_method, request_time, client_ip, request_data, response_data)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (endpoint, request_method, request_time, client_ip, request_data, response_data))

    conn.commit()
    conn.close()

def fetch_latest_logs(limit=10):
    """Fetch the latest logs from the database."""
    conn = sqlite3.connect("file_info.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT endpoint, request_method, request_time, client_ip, request_data, response_data 
        FROM api_logs 
        ORDER BY request_time DESC 
        LIMIT ?
    """, (limit,))
    
    logs = cursor.fetchall()
    conn.close()
    
    # Convert logs to a structured list
    logs_data = [
        {
            "endpoint": log[0],
            "method": log[1],
            "time": log[2],
            "client_ip": log[3],
            "request_data": log[4],
            "response_data": log[5]
        }
        for log in logs
    ]
    
    return logs_data

def save_log_analysis(analysis_data):
    """Saves the log analytics to a file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_analytics_{timestamp}.json"

    with open(filename, "w") as file:
        json.dump(analysis_data, file, indent=4)

    print(f"Log analytics saved to {filename}")
    return filename