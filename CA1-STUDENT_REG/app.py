import sqlite3
from flask import Flask,render_template,request,redirect,flash

app=Flask(__name__)
app.secret_key='secret'
DATABASE='database.db'

def create_tables():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''create table if not exists Students(
        id integer primary key autoincrement,
        name text not null,
        age integer not null,
        department text not null
    )''')
    conn.commit()
    conn.close()
@app.route('/')
def home():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''select * from  Students''')
    students=cursor.fetchall()
    conn.close()
    return render_template('index.html',students=students)
    
@app.route('/create_student',methods=['GET','POST'])
def create_student():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        dep=request.form['department']
        cursor.execute('''insert into Students(name,age,department) values (?,?,?)''',(name,age,dep))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('create_student.html')

@app.route('/edit_student',methods=['GET','POST'])
def edit_student():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''select * from Students''')
    students=cursor.fetchall()
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        age=request.form['age']
        dep=request.form['department']
        cursor.execute('''update Students set name=?,age=?,department=? where id=?''',(name,age,dep,id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('edit_student.html',students=students)

@app.route('/delete_student',methods=['GET','POST'])
def delete_student():
    conn=sqlite3.connect(DATABASE)
    cursor=conn.cursor()
    cursor.execute('''select * from Students''')
    students=cursor.fetchall()
    if request.method=='POST':
        id=request.form['id']
        cursor.execute('''delete from Students where id=?''',(id))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('delete_student.html',students=students)
if __name__=="__main__":
    create_tables()
    app.run(debug=True)