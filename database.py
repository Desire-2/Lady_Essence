import sqlite3

def init_db():
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE,
            full_name TEXT,
            is_parent INTEGER DEFAULT 0,
            language TEXT DEFAULT 'Kinyarwanda',
            sms_reminders INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS children (
            child_id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_phone TEXT,
            child_name TEXT,
            cycle_length INTEGER,
            last_period_date TEXT,
            FOREIGN KEY(parent_phone) REFERENCES users(phone_number)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cycle_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            cycle_length INTEGER,
            last_period_date TEXT,
            next_period_date TEXT,
            ovulation_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            feedback TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planetary_guidance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            guidance TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_parent(phone_number, full_name):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO users (phone_number, full_name, is_parent)
        VALUES (?, ?, 1)
    """, (phone_number, full_name))
    conn.commit()
    conn.close()

def save_child(phone_number, child_name, cycle_length, last_period_date):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO children (parent_phone, child_name, cycle_length, last_period_date)
        VALUES (?, ?, ?, ?)
    """, (phone_number, child_name, cycle_length, last_period_date))
    conn.commit()
    conn.close()

def get_children(phone_number):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM children WHERE parent_phone = ?
    """, (phone_number,))
    children = cursor.fetchall()
    conn.close()
    return children

def update_account(phone_number, full_name=None, language=None, sms_reminders=None):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    updates = []
    params = []
    if full_name:
        updates.append("full_name = ?")
        params.append(full_name)
    if language:
        updates.append("language = ?")
        params.append(language)
    if sms_reminders is not None:
        updates.append("sms_reminders = ?")
        params.append(sms_reminders)
    params.append(phone_number)
    
    if updates:
        cursor.execute(f"""
            UPDATE users SET {', '.join(updates)} WHERE phone_number = ?
        """, params)
        conn.commit()
    conn.close()

def delete_account(phone_number):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE phone_number = ?", (phone_number,))
    cursor.execute("DELETE FROM children WHERE parent_phone = ?", (phone_number,))
    conn.commit()
    conn.close()

def get_dashboard_data(phone_number):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM children WHERE parent_phone = ?", (phone_number,))
    children = cursor.fetchall()

    conn.close()
    return user, children

def delete_child(phone_number, child_id):
    conn = sqlite3.connect("menstrual_tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM children WHERE parent_phone = ? AND child_id = ?", (phone_number, child_id))
    conn.commit()
    conn.close()

