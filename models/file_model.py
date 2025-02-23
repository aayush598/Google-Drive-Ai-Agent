import sqlite3
from models.database import connect_db

def insert_file(file_id, file_name, mime_type, parent_folder, created_time, modified_time, is_folder, category=None):
    """Inserts a file record into the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO files (file_id, file_name, mime_type, parent_folder, created_time, modified_time, is_folder, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (file_id, file_name, mime_type, parent_folder, created_time, modified_time, is_folder, category))
    conn.commit()
    conn.close()

def get_all_files():
    """Retrieves all files from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files")
    files = cursor.fetchall()
    conn.close()
    return files

def update_file_category(file_id, category):
    """Updates the category of a file in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE files SET category = ? WHERE file_id = ?", (category, file_id))
    conn.commit()
    conn.close()

def delete_file(file_id):
    """Deletes a file record from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id,))
    conn.commit()
    conn.close()
