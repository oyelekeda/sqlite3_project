def add_student():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    dob = dob_entry.get()

    conn = psycopg2.connect("dbname=yourdbname user=youruser password=yourpassword")
    cur = conn.cursor()
    cur.execute("INSERT INTO Students (first_name, last_name, date_of_birth) VALUES (%s, %s, %s)", 
                (first_name, last_name, dob))
    conn.commit()
    cur.close()
    conn.close()

    update_student_table()

root = Tk()
first_name_label = Label(root, text="First Name")
first_name_label.pack()
first_name_entry = Entry(root)
first_name_entry.pack()

last_name_label = Label(root, text="Last Name")
last_name_label.pack()
last_name_entry = Entry(root)
last_name_entry.pack()

dob_label = Label(root, text="Date of Birth")
dob_label.pack()
dob_entry = Entry(root)
dob_entry.pack()

add_button = Button(root, text="Add Student", command=add_student)
add_button.pack()

root.mainloop()
