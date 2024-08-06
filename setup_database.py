import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('detection_log.db')
cursor = conn.cursor()

# Create a table for detection logs
cursor.execute('''
CREATE TABLE IF NOT EXISTS detection_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER UNIQUE,
    detection_time TEXT
)
''')

# Commit and close
conn.commit()
conn.close()
