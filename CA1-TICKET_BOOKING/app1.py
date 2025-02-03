import sqlite3

# Connect to the database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Check for any indexes on the 'stage_event_show' table
cursor.execute('select * from booking')
bookings=cursor.fetchall()
conn.close()
print(bookings)
