from flask import Flask, render_template, request, redirect, session, url_for
import requests
import os
from dotenv import load_dotenv
import sqlite3
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'any-secret-key'
app.config['SESSION_CLEARED'] = False

# Use absolute path for the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db():
    return sqlite3.connect(DB_PATH)

@app.before_request
def clear_session_on_start():
    if not app.config['SESSION_CLEARED']:
        session.clear()
        app.config['SESSION_CLEARED'] = True

@app.route('/')
def index():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM quotes")
    quotes = cur.fetchall()
    quote = random.choice(quotes)
    username = session.get('username')
    return render_template('index.html', quote=quote, username=username)

@app.route('/search', methods=['POST'])
def search():
    author = request.form['author'].strip()
    if not author:
        return render_template('index.html', quote=None, message="Please Enter Author's name.", results=None, username=session.get('username'))
    con = get_db()
    cur = con.cursor()
    # Case-insensitive search for author
    cur.execute("SELECT * FROM quotes WHERE LOWER(author) LIKE ?", ('%' + author.lower() + '%',))
    results = cur.fetchall()
    if not results:
        message = f'No quotes found for author \"{author}\". Please try another name.'
    else:
        message = None
    return render_template('index.html', results=results, quote=None, message=message, username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('auth.html', login_error="Invalid credentials", show_signup=False)
    return render_template('auth.html', show_signup=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')
        confirm_password = request.form.get('confirm_password', '')
        if password != confirm_password:
            return render_template('auth.html', register_error="Passwords do not match", show_signup=True)
        con = get_db()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            con.commit()
            return redirect(url_for('login'))
        except:
            return render_template('auth.html', register_error="User already exists", show_signup=True)
    return render_template('auth.html', show_signup=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)