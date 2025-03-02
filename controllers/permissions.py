import sqlite3
from flask import Blueprint, jsonify, render_template

# Flask Blueprint for permissions
permissions_bp = Blueprint('permissions', __name__)

# Connect to SQLite database
conn = sqlite3.connect('file_info.db', check_same_thread=False)
cursor = conn.cursor()

# Ensure permissions table exists
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
conn.commit()

def fetch_permissions(file_id,drive):
    """Fetches permissions of a file from Google Drive."""
    try:
        file = drive.CreateFile({'id': file_id})
        file.FetchMetadata(fields="permissions")
        return file['permissions']
    except Exception as e:
        print(f"Error fetching permissions for {file_id}: {e}")
        return []

# @permissions_bp.route("/fetch-permissions", methods=["GET"])
# def fetch_all_permissions(drive):
#     """Fetches permissions for all files and stores them in SQLite."""
#     cursor.execute("SELECT file_id FROM files")
#     file_ids = [row[0] for row in cursor.fetchall()]

#     for file_id in file_ids:
#         permissions = fetch_permissions(file_id,drive)
#         for permission in permissions:
#             email = permission.get('emailAddress', 'N/A')
#             role = permission.get('role', 'N/A')
#             perm_type = permission.get('type', 'N/A')

#             cursor.execute('''
#                 INSERT OR IGNORE INTO permissions (file_id, email_address, role, type)
#                 VALUES (?, ?, ?, ?)
#             ''', (file_id, email, role, perm_type))
#             conn.commit()

#     return jsonify({"message": "Permissions updated successfully!"})


def fetch_all_permissions(drive):
    """Fetches permissions for all files and stores them in SQLite."""
    cursor.execute("SELECT file_id FROM files")
    file_ids = [row[0] for row in cursor.fetchall()]
    
    all_permissions = []
    
    for file_id in file_ids:
        permissions = fetch_permissions(file_id, drive)
        for permission in permissions:
            email = permission.get('emailAddress', 'N/A')
            role = permission.get('role', 'N/A')
            perm_type = permission.get('type', 'N/A')

            cursor.execute('''
                INSERT OR IGNORE INTO permissions (file_id, email_address, role, type)
                VALUES (?, ?, ?, ?)
            ''', (file_id, email, role, perm_type))
            conn.commit()

            all_permissions.append({
                "file_id": file_id,
                "email_address": email,
                "role": role,
                "type": perm_type
            })

    return all_permissions  # Return Python dictionary instead of `jsonify()`


@permissions_bp.route("/view-permissions", methods=["GET"])
def view_permissions():
    """Displays file permissions from SQLite."""
    cursor.execute("""
        SELECT files.file_name, permissions.email_address, permissions.role, permissions.type
        FROM permissions
        JOIN files ON permissions.file_id = files.file_id
    """)
    permissions_data = cursor.fetchall()
    
    return render_template("permissions.html", permissions=permissions_data)