import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            full_name TEXT,
            phone_number TEXT,
            region TEXT,
            subject TEXT,
            source TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Try to add username column if it doesn't exist (for migration)
    try:
        cursor.execute('ALTER TABLE applications ADD COLUMN username TEXT')
    except sqlite3.OperationalError:
        pass # Column already exists
        
    conn.commit()
    conn.close()

def add_application(user_id, username, full_name, phone_number, region, subject, source):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (user_id, username, full_name, phone_number, region, subject, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, username, full_name, phone_number, region, subject, source))
    conn.commit()
    conn.close()

def get_all_applications():
    """Returns all applications sorted by creation date descending."""
    conn = sqlite3.connect(DB_PATH)
    # Using generic fetch to pass to pandas later
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, full_name, phone_number, region, subject, source, created_at 
        FROM applications 
        ORDER BY created_at DESC
    ''')
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return rows, columns
