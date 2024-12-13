import sqlite3

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect("candidate.db")  # Creates a file-based SQLite database
    return conn

# Function to create the table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        last_name TEXT NOT NULL,
        dob TEXT,
        age INTEGER,
        gender TEXT,
        passport_status TEXT,
        mobile TEXT,
        pan TEXT,
        visa_status TEXT,
        email TEXT,
        emergency_contact_name TEXT,
        emergency_contact_mobile TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to insert candidate details
def insert_candidate(first_name, middle_name, last_name, dob, age, mobile, gender, email, emergency_name, emergency_mobile):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Users (first_name, middle_name, last_name, dob, age, mobile, gender, email, emergency_contact_name, emergency_contact_mobile)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    ''', (first_name, middle_name, last_name, dob, age, mobile, gender, email, emergency_name, emergency_mobile))
    conn.commit()
    conn.close()

# Function to fetch all candidates
def fetch_candidates():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_candidates(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Users
        WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_candidates():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE Users")
    rows = cursor.fetchall()
    conn.close()
    return rows

