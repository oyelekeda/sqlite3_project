def calculate_average(subject):
    conn = psycopg2.connect("dbname=yourdbname user=youruser password=yourpassword")
    cur = conn.cursor()
    cur.execute("SELECT AVG(score) FROM Results WHERE subject = %s", (subject,))
    average_score = cur.fetchone()[0]
    cur.close()
    conn.close()
    return average_score


average_label = Label(root, text="Average Score:")
average_label.pack()

average_score_label = Label(root, text=str(calculate_average("Math")))
average_score_label.pack()
