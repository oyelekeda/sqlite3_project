import sqlite3

def connect_to_db():
    try:
        connection = sqlite3.connect("database.db")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_table():
    connection = connect_to_db()
    if connection is None:
        return "Database connection failed"
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE student_results (
            student_id INTEGER PRIMARY KEY,
            subject_code TEXT NOT NULL,
            marks INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
        """)
        connection.commit()
        return "Table created successfully"
    except Exception as e:
        return f"Error creating table: {e}"
    finally:
        cursor.close()
        connection.close()

def insert_student_result(student_id, subject_code, marks, grade):
    connection = connect_to_db()
    if connection is None:
        return "Database connection failed"
    
    try:
        cursor = connection.cursor()

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID")
        if not isinstance(subject_code, str) or len(subject_code) != 6:
            raise ValueError("Invalid subject code")
        if not (0 <= marks <= 100):
            raise ValueError("Marks should be between 0 and 100")
        if grade not in ['A', 'B', 'C', 'D', 'E', 'F']:
            raise ValueError("Invalid grade")

        insert_query = """
        INSERT INTO student_results (student_id, subject_code, marks, grade)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(insert_query, (student_id, subject_code, marks, grade))
        connection.commit()
        return "Result inserted successfully"
    
    except Exception as e:
        return f"Error: {e}"
    
    finally:
        cursor.close()
        connection.close()

def update_student_result(student_id, subject_code, new_marks, new_grade):
    connection = connect_to_db()
    if connection is None:
        return "Database connection failed"
    
    try:
        cursor = connection.cursor()

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID")
        if not isinstance(subject_code, str) or len(subject_code) != 6:
            raise ValueError("Invalid subject code")
        if not (0 <= new_marks <= 100):
            raise ValueError("Marks should be between 0 and 100")
        if new_grade not in ['A', 'B', 'C', 'D', 'E', 'F']:
            raise ValueError("Invalid grade")

        update_query = """
        UPDATE student_results
        SET marks = ?, grade = ?
        WHERE student_id = ? AND subject_code = ?
        """
        cursor.execute(update_query, (new_marks, new_grade, student_id, subject_code))
        connection.commit()
        
        if cursor.rowcount == 0:
            return "No matching record found to update"
        
        return "Result updated successfully"
    
    except Exception as e:
        return f"Error: {e}"
    
    finally:
        cursor.close()
        connection.close()

def delete_student_result(student_id, subject_code):
    connection = connect_to_db()
    if connection is None:
        return "Database connection failed"
    
    try:
        cursor = connection.cursor()

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID")
        if not isinstance(subject_code, str) or len(subject_code) != 6:
            raise ValueError("Invalid subject code")

        delete_query = """
        DELETE FROM student_results
        WHERE student_id = ? AND subject_code = ?
        """
        cursor.execute(delete_query, (student_id, subject_code))
        connection.commit()

        if cursor.rowcount == 0:
            return "No matching record found to delete"
        
        return "Result deleted successfully"
    
    except Exception as e:
        return f"Error: {e}"
    
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print(create_table())
    print(insert_student_result(1, "SUB001", 85, "A"))#1 student id #SUB001 is a subject code.  #85 is updated score  #A is a grade letter
    print(update_student_result(1, "SUB001", 90, "A"))#1 student id #SUB001 is a subject code.  #93 is updated score  #A is a grade letter
    print(delete_student_result(1, "SUB001"))#SUB001 is a subject code.  #1 student id
