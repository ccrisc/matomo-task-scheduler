from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from db.db_connection import get_connection
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            conn.close()
    else:
        user = None
    return User(user['id'], user['username']) if user else None


@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/api_calls')
@login_required
def api_calls():
    conn = get_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM api_calls ORDER BY timestamp DESC")
            api_calls = cursor.fetchall()
            conn.close()
    else:
        api_calls = []

    return render_template('api_calls.html', api_calls=api_calls)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    error_message = None  # Variable to store error messages

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        if conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                conn.close()

            if user:
                try:
                    if check_password_hash(user['password_hash'], password):
                        user_obj = User(user['id'], user['username'])
                        login_user(user_obj)
                        return redirect(url_for('dashboard'))
                    else:
                        error_message = 'Incorrect password. Please try again.'
                except ValueError as e:
                    error_message = f"Password verification failed: {str(e)}"
            else:
                error_message = 'Username not found. Please try again.'
        else:
            error_message = 'Database connection error.'

    return render_template('login.html', error_message=error_message)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
