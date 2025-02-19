import sqlite3

def search_files_by_category(category_input):
    # Connect to SQLite database
    conn = sqlite3.connect('file_info.db', check_same_thread=False)
    cursor = conn.cursor()

    # Query to find files where category contains the input text
    cursor.execute("SELECT file_name FROM files WHERE category LIKE ?", ('%' + category_input + '%',))
    matching_files = [row[0] for row in cursor.fetchall()]

    conn.close()
    return matching_files
