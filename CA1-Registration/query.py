import sqlite3

def check_data():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_data()
