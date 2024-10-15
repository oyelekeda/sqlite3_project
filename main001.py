import sqlite3

def CREATE_TABLE_Users():
    query = """
    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(70) NOT NULL,
        seat VARCHAR(20) NOT NULL CHECK (seat IN ('admin', 'teacher')),
        Script VARCHAR(20) NOT NULL,
        Addmision VARCHAR(20) NOT NULL
    );
    """
    return query

def CREATE_TABLE_Students():
    query = """
    CREATE TABLE Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        seat_no VARCHAR(20) UNIQUE NOT NULL,
        Script VARCHAR(20) NOT NULL,
        admission_no VARCHAR(20) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        school VARCHAR(10) NOT NULL
    );
    """
    return query

def CREATE_TABLE_Results():
    query = """
    CREATE TABLE Results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject VARCHAR(50) NOT NULL,
        marks_obtained INTEGER CHECK (marks_obtained >= 0),
        max_marks INTEGER CHECK (max_marks > 0),
        exam_date DATE NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
    );
    """
    return query


def create_tables():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    
    cursor.execute(CREATE_TABLE_Users())
    cursor.execute(CREATE_TABLE_Students())
    cursor.execute(CREATE_TABLE_Results())

    
    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
