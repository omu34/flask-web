from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras

auth = Blueprint('auth', __name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="astudents",
        user="postgres",
        password="55",
        host="localhost",
        port="55"
    )
    return conn

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        try:
            cur.execute('INSERT INTO signup (fullname, username, email, password) VALUES (%s, %s, %s, %s)', 
                        (fullname, username, email, password))
            conn.commit()
            flash('User registered successfully!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            conn.rollback()
            flash(f'Error: {str(e)}')
        finally:
            cur.close()
            conn.close()
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute('SELECT * FROM signup WHERE username = %s', (username,))
        user = cur.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!')
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect username or password')
        
        cur.close()
        conn.close()
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

