import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('detection_log.db')
cursor = conn.cursor()

# Query the database
cursor.execute('SELECT * FROM detection_log')
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)

conn.close()
