import bcrypt
import psycopg2
from tkinter import *

def hash_password(password):
    return bcrypt.hashpw(password.encode('2023/46611'),  bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('2023/46611'), stored_password)

def register_user(username, password):
    conn = psycopg2.connect("dbname=yourdbname user=youruser password=yourpassword")
    cur = conn.cursor()
    password_hash = hash_password(password)
    cur.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    cur.close()
    conn.close()

def login_user(username, password):
    conn = psycopg2.connect("dbname=yourdbname user=youruser password=yourpassword")
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM Users WHERE username = %s", (username,))
    stored_password = cur.fetchone()[0]
    conn.close()
    return verify_password(stored_password, password)
