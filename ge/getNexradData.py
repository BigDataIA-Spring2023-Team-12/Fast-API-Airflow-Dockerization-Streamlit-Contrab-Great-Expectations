import sqlite3
import csv

conn = sqlite3.connect("../streamlit/meta_data.db")
cur = conn.cursor()

cur.execute("SELECT * from nexrad")
rows = cur.fetchall()

with open("../ge/great_expectations/data/nexrad.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([i[0] for i in cur.description])  # write the header row
    writer.writerows(rows)

cur.close()
conn.close()
