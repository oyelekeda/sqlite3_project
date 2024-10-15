import sqlite3

def CREATE_TABLE_Users():
    query = """
    CREATE TABLE IF NOT EXISTS Users (
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
    CREATE TABLE IF NOT EXISTS Students (
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
    CREATE TABLE IF NOT EXISTS Results (
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


import tkinter as tk
from tkinter import messagebox
import hashlib 
import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)""")
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == "" or password == "":
        messagebox.showerror("Error", "Both fields are required!")
        return
    
    hashed_pw = hash_password(password)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        messagebox.showinfo("Success", "Welcome, your registered is complete!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This username has already beeen created!")
    finally:
        conn.close()

def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Both fields are required!")
        return
    
    hashed_pw = hash_password(password)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    result = c.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "incorrect login information!")

root = tk.Tk()
root.title("User Authentication")

label_username = tk.Label(root, text="Username:")
label_username.grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)


label_password = tk.Label(root, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)


btn_register = tk.Button(root, text="Register", command=register_user)
btn_register.grid(row=2, column=0, padx=10, pady=10)

btn_login = tk.Button(root, text="Login", command=login_user)
btn_login.grid(row=2, column=1, padx=10, pady=10)

init_db()
root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentRecordsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Records Management")
        self.root.geometry("1500x800")

        self.student_data = []

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.name_label = tk.Label(self.frame, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.age_label = tk.Label(self.frame, text="Age:")
        self.age_label.grid(row=1, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.frame)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        self.grade_label = tk.Label(self.frame, text="Grade:")
        self.grade_label.grid(row=2, column=0, padx=10, pady=5)
        self.grade_entry = tk.Entry(self.frame)
        self.grade_entry.grid(row=2, column=1, padx=10, pady=5)


        self.add_button = tk.Button(self.frame, text="Add", command=self.add_student)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self.frame, text="Update", command=self.update_student)
        self.update_button.grid(row=5, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.frame, text="Delete", command=self.delete_student)
        self.delete_button.grid(row=5, column=2, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Age", "Grade"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Grade", text="Grade")
        self.tree.pack(pady=20)

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()

        if name and age.isdigit() and grade:
            self.student_data.append((name, int(age), grade))
            self.refresh_treeview()
            self.clear_form()
        else:
            messagebox.showerror("Input Error", "Please enter valid data.")

    def update_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            name = self.name_entry.get()
            age = self.age_entry.get()
            grade = self.grade_entry.get()

            if name and age.isdigit() and grade:
                selected_index = self.tree.index(selected_item[0])
                self.student_data[selected_index] = (name, int(age), grade)
                self.refresh_treeview()
                self.clear_form()
            else:
                messagebox.showerror("Input Error", "Please enter valid data.")
        else:
            messagebox.showerror("Selection Error", "Please select a student to update.")

    def delete_student(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_index = self.tree.index(selected_item[0])
            del self.student_data[selected_index]
            self.refresh_treeview()
            self.clear_form()
        else:
            messagebox.showerror("Selection Error", "Please select a student to delete.")

    def refresh_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in self.student_data:
            self.tree.insert("", "end", values=student)

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_index = self.tree.index(selected_item[0])
            selected_student = self.student_data[selected_index]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, selected_student[0])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, selected_student[1])
            self.grade_entry.delete(0, tk.END)
            self.grade_entry.insert(0, selected_student[2])

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordsApp(root)
    root.mainloop()


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


students_data = [
     {"name": "Olabiyi", "Math": 80, "English": 60, "chemistry": 88, "biology":78},
    {"name": "Samuel", "Math": 72, "English": 95, "chemistry": 71, "biology":90},
    {"name": "Temidayo", "Math": 90, "English": 87, "chemistry": 83, "biology":89}

]

def calculate_average(student):
    scores = [score for subject, score in student.items() if subject != "name"]
    average = sum(scores) / len(scores)
    return average
def top_performers(students_data):
    students_with_avg = [(student['name'], calculate_average(student)) for student in students_data]
    students_with_avg.sort(key=lambda x: x[1], reverse=True)
    return students_with_avg
import tkinter as tk

def generate_report():
    report_text.delete(3.0, tk.END)  
    
    report = top_performers(students_data)
    
    for name, avg in report:
        report_text.insert(tk.END, f"Student: {name}, Average: {avg:.2f}\n")

root = tk.Tk()
root.title("Student Report Generator")

generate_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_button.pack(pady=10)

report_text = tk.Text(root, height=10, width=50)
report_text.pack(pady=10)

students_data = [
     {"name": "Olabiyi", "Math": 80, "English": 60, "chemistry": 88, "biology":78},
    {"name": "samuel", "Math": 72, "English": 95, "chemistry": 71, "biology":90},
    {"name": "Temidayo", "Math": 90, "English": 87, "chemistry": 83, "biology":89}
]

root.mainloop()


import tkinter as tk
from tkinter import messagebox

def submit_record():
    messagebox.showinfo("Submission", "Record Submitted!")

def delete_record():
    messagebox.showinfo("Deletion", "Record Deleted!")

def display_math_results():
    messagebox.showinfo("Results", "Displaying Math Results")

def display_English_results():
    messagebox.showinfo("Results", "Displaying English Results")

def display_chemistry_results():
    messagebox.showinfo("Results", "Displaying Chemistry Results")

def display_biology_results():
    messagebox.showinfo("Results", "Displaying biology Results")


root = tk.Tk()
root.title("Exam Records")
root.geometry("700x500")
root.config(bg="light green")

title_label = tk.Label(root, text="Exam Records", font=("impact", 24), fg="black", bg="white")
title_label.grid(row=0, column=0, columnspan=3, pady=10)

tk.Label(root, text="Name", bg="light green").grid(row=1, column=0, padx=10, pady=5, sticky="e")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=1, column=1, padx=10)

tk.Label(root, text="Gender", bg="light green").grid(row=2, column=0, padx=10, pady=5, sticky="e")
gender_var = tk.StringVar()
male_rb = tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", bg="white", fg="red")
male_rb.grid(row=2, column=1, sticky="w")
female_rb = tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", bg="white", fg="brown")
female_rb.grid(row=2, column=1, sticky="e")

tk.Label(root, text="Seat Number", bg="light green").grid(row=3, column=0, padx=10, pady=5, sticky="e")
roll_entry = tk.Entry(root, width=30)
roll_entry.grid(row=3, column=1, padx=10)

tk.Label(root, text="Script Number", bg="light green").grid(row=4, column=0, padx=10, pady=5, sticky="e")
roll_entry = tk.Entry(root, width=30)
roll_entry.grid(row=4, column=1, padx=10)

tk.Label(root, text="Addmision_Number", bg="light green").grid(row=5, column=0, padx=10, pady=5, sticky="e")
roll_entry = tk.Entry(root, width=30)
roll_entry.grid(row=5, column=1, padx=10)

tk.Label(root, text="Mathematics", bg="light green").grid(row=6, column=0, padx=10, pady=5, sticky="e")
math_entry = tk.Entry(root, width=30)
math_entry.grid(row=6, column=1, padx=10)

tk.Label(root, text="English", bg="light green").grid(row=7, column=0, padx=10, pady=5, sticky="e")
physics_entry = tk.Entry(root, width=30)
physics_entry.grid(row=7, column=1, padx=10)

tk.Label(root, text="Chemistry", bg="light green").grid(row=8, column=0, padx=10, pady=5, sticky="e")
chemistry_entry = tk.Entry(root, width=30)
chemistry_entry.grid(row=8, column=1, padx=10)
tk.Label(root, text="Biology", bg="light green").grid(row=9, column=0, padx=10, pady=5, sticky="e")
chemistry_entry = tk.Entry(root, width=30)
chemistry_entry.grid(row=9, column=1, padx=10)


submit_btn = tk.Button(root, text="Submit", command=submit_record, bg="grey", fg="light green", width=30)
submit_btn.grid(row=10, column=1, pady=10)

delete_btn = tk.Button(root, text="Delete A Record", command=delete_record, bg="grey", fg="light green", width=20)
delete_btn.grid(row=11, column=1, pady=5)

display_math_btn = tk.Button(root, text="Display Maths Results", command=display_math_results, bg="grey", fg="light green", width=20)
display_math_btn.grid(row=2, column=3, padx=10, pady=5)

display_physics_btn = tk.Button(root, text="Display English Results", command=display_English_results, bg="grey", fg="light green", width=20)
display_physics_btn.grid(row=3, column=3, padx=10, pady=5)

display_chemistry_btn = tk.Button(root, text="Display Chemistry Results", command=display_chemistry_results, bg="grey", fg="light green", width=20)
display_chemistry_btn.grid(row=4, column=3, padx=10, pady=5)

root.mainloop()



