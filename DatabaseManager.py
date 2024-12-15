import sqlite3

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect("candidate.db")  # Creates a file-based SQLite database
    return conn

# to get the candidate id
def get_last_candidate_id():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(candidate_id) FROM Candidates")
    last_id = cursor.fetchone()[0]
    return last_id

# Function to create the tables if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Create the Candidates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Candidates (
            candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            dob TEXT,
            age TEXT,
            gender TEXT,
            passport TEXT,
            mobile TEXT,
            pan TEXT,
            visa_status TEXT,
            email TEXT,
            current_street TEXT,
            current_city TEXT,
            current_state TEXT,
            current_zip TEXT,
            current_country TEXT,
            permanent_street TEXT,
            permanent_city TEXT,
            permanent_state TEXT,
            permanent_zip TEXT,
            permanent_country TEXT,
            emergency_contact_name TEXT,
            emergency_contact_number TEXT,
            relocation_availability BOOLEAN
        )
    ''')

    # Create the Education table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Education (
            education_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            sr_no TEXT,
            school_university_name TEXT,
            qualification TEXT,
            percentage_or_cgpa TEXT,
            pass_out_year TEXT,
            FOREIGN KEY (candidate_id) REFERENCES Candidates(candidate_id)
        )
    ''')

    # Create the Training table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Training (
            training_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            program TEXT,
            contents TEXT,
            organized_by TEXT,
            duration TEXT,
            FOREIGN KEY (candidate_id) REFERENCES Candidates(candidate_id)
        )
    ''')

    # Create the Certifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Certifications (
            certification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            certification TEXT,
            duration TEXT,
            FOREIGN KEY (candidate_id) REFERENCES Candidates(candidate_id)
        )
    ''')

    # Create the Family table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Family (
            family_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            relation TEXT,
            occupation_profession TEXT,
            resident_location TEXT,
            FOREIGN KEY (candidate_id) REFERENCES Candidates(candidate_id)
        )
    ''')

    # Create the References table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reference (
            reference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            name TEXT,
            mobile TEXT,
            email TEXT,
            FOREIGN KEY (candidate_id) REFERENCES Candidates(candidate_id)
        )
        ''')

    conn.commit()
    conn.close()

# Function to insert candidate details
def insert_candidate(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Candidates (
            first_name, middle_name, last_name, dob, age, gender, passport, mobile, pan, visa_status, email,
            current_street, current_city, current_state, current_zip, current_country,
            permanent_street, permanent_city, permanent_state, permanent_zip, permanent_country,
            emergency_contact_name, emergency_contact_number, relocation_availability
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

# Function to insert education details
def insert_into_education(data):
    last_id = get_last_candidate_id()
    data = (last_id, *data) 
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Education (
            candidate_id, sr_no, school_university_name, qualification, percentage_or_cgpa, pass_out_year
        )
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

# To make a reference
def insert_into_references(data):
    last_id = get_last_candidate_id()
    data = (last_id, *data) 
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Reference (
            candidate_id, name, mobile, email
        )
        VALUES (?, ?, ?, ?)
    ''', data)
    conn.commit()

# Search andidate from the reference table
def search_candidates(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Reference
        WHERE name LIKE ? OR email LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    # print("test")
    return rows

# Function to fetch all candidates
def fetch_candidates():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reference")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to fetch candidates details
def get_candidates(candidates_id):
    # print(candidates_id)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Candidates WHERE candidate_id = "+str(candidates_id))   
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to fetch educational details
def get_education(candidates_id):
    # print(candidates_id)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Education WHERE candidate_id = "+str(candidates_id))   
    rows = cursor.fetchall()
    conn.close()
    return rows

