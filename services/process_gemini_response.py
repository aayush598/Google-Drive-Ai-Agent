import re
import sqlite3

def process_gemini_response(gemini_response):
    """
    Processes the response from Gemini API and updates the database with file categories.
    """
    conn = sqlite3.connect('file_info.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Ensure 'category' column exists in the database
    cursor.execute("PRAGMA table_info(files)")
    columns = [col[1] for col in cursor.fetchall()]
    if "category" not in columns:
        cursor.execute("ALTER TABLE files ADD COLUMN category TEXT")
        conn.commit()
    
    if gemini_response is None:
        return {}
    
    categorized_data = {}
    categorized_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
    
    # Use regex to match file names and categories
    pattern = r'([\w.-]+):\s*(.+)'
    matches = re.findall(pattern, categorized_text)
    
    for file_name, category in matches:
        file_name = file_name.strip().replace("**", "").replace("*", "")
        category = category.strip().replace("**", "")
        
        cursor.execute('SELECT file_id FROM files WHERE file_name = ?', (file_name,))
        result = cursor.fetchone()
        
        if result:
            file_id = result[0]
            cursor.execute('UPDATE files SET category = ? WHERE file_id = ?', (category, file_id))
            conn.commit()
            categorized_data[file_name] = category
            print(f"Updated {file_name} (ID: {file_id}) with category: {category}")
        else:
            print(f"File '{file_name}' not found in the database. Skipping update.")
    
    print("Categorized Data Stored in Database:", categorized_data)
    conn.close()
    return categorized_data
