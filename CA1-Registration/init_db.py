import sqlite3

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')

conn.commit()
conn.close()
