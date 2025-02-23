import sqlite3

def find_duplicates():
    """
    Identifies duplicate file names in the database.
    Returns a dictionary with file names as keys and duplicate counts as values.
    """
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT file_name, COUNT(*) 
        FROM files 
        GROUP BY file_name 
        HAVING COUNT(*) > 1
    """)
    
    duplicates = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return duplicates

def get_duplicates():
    """
    Retrieves duplicate file entries from the database.
    """
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT file_id, file_name 
        FROM files 
        WHERE file_name IN (
            SELECT file_name FROM files GROUP BY file_name HAVING COUNT(*) > 1
        )
    """)
    
    duplicates = cursor.fetchall()
    conn.close()
    return duplicates