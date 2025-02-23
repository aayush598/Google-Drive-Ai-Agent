import sqlite3

def search_files_by_category(category_input):
    """
    Searches for files in the database that match the given category.
    """
    print(f"Searching for files with category '{category_input}'")
    conn = sqlite3.connect('file_info.db', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT file_name FROM files WHERE category LIKE ?", ('%' + category_input + '%',))
    matching_files = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    print(f"Matching files for category '{category_input}': {matching_files}")
    return matching_files