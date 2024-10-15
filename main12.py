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
