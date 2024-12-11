from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Needed for session management

# Initialize database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                mobile TEXT NOT NULL,
                student_class TEXT NOT NULL,
                dob DATE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/scholarships')
def scholarships():
    if 'username' in session:
        return render_template('scholarships.html')
    else:
        return redirect(url_for('login'))

@app.route('/save_profile', methods=['POST'])
def save_profile():
    if 'username' in session:
        data = request.get_json()
        name = data.get('name')
        gender = data.get('gender')
        email = data.get('email')
        mobile = data.get('mobile')
        student_class = data.get('studentClass')
        dob = data.get('dob')
        password = data.get('password')

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, gender, email, mobile, student_class, dob, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, gender, email, mobile, student_class, dob, password))
            conn.commit()

        return jsonify({'message': 'Profile saved successfully', 'success': True})
    else:
        return jsonify({'message': 'Unauthorized', 'success': False}), 401

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        gender = data.get('gender')
        email = data.get('email')
        mobile = data.get('mobile')
        student_class = data.get('studentClass')
        dob = data.get('dob')
        password = data.get('password')

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, gender, email, mobile, student_class, dob, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, gender, email, mobile, student_class, dob, password))
            conn.commit()

        return jsonify({'message': 'Registration successful', 'success': True})
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (username, password))
            user = cursor.fetchone()

            if user:
                session['username'] = username
                return jsonify({'message': 'Login successful'}), 200
            else:
                return jsonify({'message': 'Login failed'}), 401
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')
@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
