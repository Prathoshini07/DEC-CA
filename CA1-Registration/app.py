# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from sqlite3 import IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        
        if not name or not email:
            flash('Name and email are required!')
            return redirect(url_for('register'))
            
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                        (id, name, email))
            conn.commit()
            flash('User successfully registered!')
            return redirect(url_for('index'))
        except IntegrityError:
            flash('Error: Email already exists or invalid ID!')
            return redirect(url_for('register'))
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if not name or not email:
            flash('Name and email are required!')
            return redirect(url_for('edit', id=id))
            
        try:
            conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?',
                        (name, email, id))
            conn.commit()
            flash('User successfully updated!')
            return redirect(url_for('index'))
        except IntegrityError:
            flash('Error: Email already exists!')
            return redirect(url_for('edit', id=id))
        finally:
            conn.close()
    
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('User successfully deleted!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)