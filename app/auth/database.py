import sqlite3
import os
import hashlib

def get_db_path():
    return os.path.join(os.path.dirname(__file__), 'users.db')

def init_db():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    # Create detection history table
    c.execute('''CREATE TABLE IF NOT EXISTS detection_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        detection_type TEXT NOT NULL,
        input_data TEXT NOT NULL,
        result TEXT NOT NULL,
        prediction_probability REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                  (username, email, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True
    return False

def save_detection_result(username, detection_type, input_data, result, prediction_probability=None):
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        # Get user_id
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = c.fetchone()[0]
        
        # Save detection result
        c.execute('''INSERT INTO detection_history 
            (user_id, detection_type, input_data, result, prediction_probability)
            VALUES (?, ?, ?, ?, ?)''',
            (user_id, detection_type, input_data, result, prediction_probability))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving detection result: {e}")
        return False

def get_user_history(username):
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        # Get user's detection history
        c.execute('''
            SELECT 
                detection_type,
                input_data,
                result,
                prediction_probability,
                timestamp
            FROM detection_history h
            JOIN users u ON h.user_id = u.id
            WHERE u.username = ?
            ORDER BY timestamp DESC
        ''', (username,))
        
        history = c.fetchall()
        conn.close()
        
        return history
    except Exception as e:
        print(f"Error getting user history: {e}")
        return []

def clear_user_history(username):
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        # Get user_id
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = c.fetchone()[0]
        
        # Delete all detection history for the user
        c.execute('DELETE FROM detection_history WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing user history: {e}")
        return False 