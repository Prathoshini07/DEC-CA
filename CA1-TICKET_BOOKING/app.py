import sqlite3
from flask import Flask, render_template, request, redirect,flash

app = Flask(__name__)
DATABASE = 'data.db'
app.secret_key='secret'

# Function to create tables if they don't exist
def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stage_event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        detail TEXT NOT NULL,
        organizer TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS stage_event_show (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stage_event_id INTEGER,
        start_time text,
        end_time text,
        available_seats INTEGER NOT NULL,
        FOREIGN KEY(stage_event_id) REFERENCES stage_event(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT NOT NULL,
        price DOUBLE,
        no_of_seats INTEGER NOT NULL,
        stage_event_show_id INTEGER,
        FOREIGN KEY(stage_event_show_id) REFERENCES stage_event_show(id)
    )''')

    conn.commit()
    conn.close()

# Home route - display events
@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM stage_event''')
    events = cursor.fetchall()  # Convert cursor to list
    cursor.execute('''select * from stage_event_show''')
    shows=cursor.fetchall()
    cursor.execute('''select * from booking''')
    bookings=cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events,shows=shows,bookings=bookings)

# Route to add an event
@app.route('/add_event', methods=['POST', 'GET'])
def add_event():
    if request.method == 'POST':  # Fixed condition
        name = request.form['name']
        detail = request.form['detail']
        organizer = request.form['organizer']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO stage_event (name, detail, organizer) VALUES (?, ?, ?)''', 
                       (name, detail, organizer))
        conn.commit()  # Fixed missing ()
        conn.close()   # Fixed missing ()

        return redirect('/')  # Redirect to home page after adding event

    return render_template('add_event.html')  # Show form

@app.route('/add_show',methods=['GET','POST'])
def add_show():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''select id,name from stage_event''')
    events=cursor.fetchall()
    if request.method=='POST':
        event_id=request.form['event_id']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        seats=int(request.form['available_seats'])
        cursor.execute('''insert into stage_event_show(stage_event_id,start_time,end_time,available_seats) values(?,?,?,?)''',(event_id,start_time,end_time,seats))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_show.html',events=events)

@app.route('/book',methods=['GET','POST','UPDATE'])
def book():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''select * from stage_event_show''')
    shows=cursor.fetchall()
    if request.method=="POST":
        show_event_id=request.form['show_event_id']
        customer=request.form['customer']
        price=request.form['price']
        no_of_seats=int(request.form['no_of_seats'])
        cursor.execute('''insert into booking(customer,price,no_of_seats,stage_event_show_id) values(?,?,?,?)''',(customer,price,no_of_seats,show_event_id))
        cursor.execute('''update stage_event_show set available_seats=available_seats-? where id=?''',(no_of_seats,show_event_id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('book.html',shows=shows)
@app.route('/delete',methods=['GET','POST'])
def delete():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''select * from booking''')
    bookings=cursor.fetchall()
    if request.method=='POST':
        booking_id=request.form['booking_id']
        cursor.execute('''delete from booking where booking_id=?''',(booking_id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('/delete.html',bookings=bookings)
# Run the app
if __name__ == "__main__":
    create_tables()  # Ensure tables exist
    app.run(debug=True)
