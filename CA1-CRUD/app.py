import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.secret_key = 'secret'
DATABASE = 'database.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS shows (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_id INTEGER,
                        show_time TEXT NOT NULL,
                        available_tickets INTEGER NOT NULL,
                        FOREIGN KEY(event_id) REFERENCES events(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        show_id INTEGER,
                        customer_name TEXT NOT NULL,
                        num_tickets INTEGER NOT NULL,
                        FOREIGN KEY(show_id) REFERENCES shows(id))''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    cursor.execute("SELECT s.id, e.name, s.show_time, s.available_tickets FROM shows s JOIN events e ON s.event_id = e.id")
    shows = cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events, shows=shows)
@app.route('/book/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    conn = sqlite3.connect(DATABASE)
    show = conn.execute('SELECT * FROM shows WHERE id = ?', (show_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        num_tickets = int(request.form['num_tickets'])

        if show and show[3] >= num_tickets:
            # Update available tickets
            conn.execute('UPDATE shows SET available_tickets = available_tickets - ? WHERE id = ?', (num_tickets, show_id))
            conn.commit()
            conn.close()
    
    conn.close()
    return render_template("book.html", show=show)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_event.html')

@app.route('/add_show', methods=['GET', 'POST'])
def add_show():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM events")
    events = cursor.fetchall()
    
    if request.method == 'POST':
        event_id = request.form['event_id']
        show_time = request.form['show_time']
        available_tickets = request.form['available_tickets']

        cursor.execute("INSERT INTO shows (event_id, show_time, available_tickets) VALUES (?, ?, ?)",
                       (event_id, show_time, available_tickets))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('add_show.html', events=events)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
