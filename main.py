# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                year_of_birth INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


create_table()


@app.route('/')
def index():
    return render_template('index.html', name='Flask')


@app.route('/add_details', methods=['GET', 'POST'])
def add_details():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        year_of_birth = request.form['year_of_birth']

        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO details (name, gender, year_of_birth)
                VALUES (?, ?, ?)
            ''', (name, gender, year_of_birth))
            conn.commit()
            conn.close()

        return redirect(url_for('index'))
    return render_template('add_details.html')

@app.route('/search')
def search():
    search_name = request.args.get('search_name')
    if search_name:
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM details WHERE name LIKE ?
            ''', ('%' + search_name + '%',))
            results = cursor.fetchall()
            conn.close()
            return render_template('search_results.html', results=results)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
