import sqlite3

def connect_db():
    """Creates and returns a connection to the SQLite database."""
    return sqlite3.connect('file_info.db', check_same_thread=False)

def initialize_database():
    """Creates necessary tables if they do not exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT UNIQUE,
            file_name TEXT,
            mime_type TEXT,
            parent_folder TEXT,
            created_time TEXT,
            modified_time TEXT,
            is_folder INTEGER DEFAULT 0,
            category TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT,
            email_address TEXT,
            role TEXT,
            type TEXT,
            UNIQUE(file_id, email_address)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensitive_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            analysis_time TEXT,
            description TEXT,
            risk_level TEXT,
            category TEXT,
            examples TEXT,
            remediation TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            request_method TEXT,
            request_time TEXT,
            client_ip TEXT,
            request_data TEXT,
            response_data TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
