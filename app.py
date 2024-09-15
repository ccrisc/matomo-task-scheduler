from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, send_from_directory, abort, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
from datetime import timedelta
import os
import pandas as pd
from db.db_connection import get_connection
from report_generator import generate_reports

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Configure upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'generated_reports')

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set session timeout to 30 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

def file_exists(file_name):
    """Check if the file exists in the upload folder."""
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
    return os.path.isfile(file_path)

@app.context_processor
def utility_processor():
    """Add utility functions to the Jinja2 template context."""
    return dict(file_exists=file_exists)

class User(UserMixin):
    def __init__(self, id, username, admin=False):
        self.id = id
        self.username = username
        self.admin = admin

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, username, admin FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            conn.close()
    else:
        user = None
    return User(user['id'], user['username'], user['admin']) if user else None

@app.route('/')
@login_required
def dashboard():
    conn = get_connection()
    last_api_call = None

    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM api_calls ORDER BY created_at DESC LIMIT 1")
                last_api_call = cursor.fetchone()
        finally:
            conn.close()

    return render_template('dashboard.html', last_api_call=last_api_call)

@app.route('/api_calls')
@login_required
def api_calls():
    conn = get_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM api_calls ORDER BY created_at DESC")
            api_calls = cursor.fetchall()
            conn.close()
    else:
        api_calls = []

    return render_template('api_calls.html', api_calls=api_calls)

@app.route('/stats')
@login_required
def stats():
    return render_template('stats.html')

@app.route('/api/stats', methods=['POST'])
@login_required
def get_filtered_stats():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    device_type = data.get('device_type')

    conn = get_connection()
    stats = {}
    filters = []
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT COUNT(*) AS total_visits, 
                           AVG(visit_duration) AS avg_visit_duration, 
                           device_type, browser_name 
                    FROM daily_visits WHERE TRUE
                """
                if start_date and end_date:
                    query += " AND server_time BETWEEN %s AND %s"
                    filters.extend([start_date, end_date])

                query += " GROUP BY device_type, browser_name"
                cursor.execute(query, tuple(filters))
                stats = cursor.fetchall()

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()

    return jsonify(stats), 200

@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    conn = get_connection()
    users = []

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (username, encrypted_password) VALUES (%s, %s)",
                        (username, hashed_password)
                    )
                    conn.commit()
            finally:
                conn.close()
        return redirect(url_for('manage_users'))

    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM users ORDER BY id ASC")
                users = cursor.fetchall()
        finally:
            conn.close()

    return render_template('users.html', users=users)

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    conn = get_connection()
    user = None

    if request.method == 'POST':
        username = request.form['username']
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE users SET username = %s WHERE id = %s",
                        (username, id)
                    )
                    conn.commit()
            finally:
                conn.close()
        return redirect(url_for('users'))

    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id, username FROM users WHERE id = %s", (id,))
                user = cursor.fetchone()
        finally:
            conn.close()

    return render_template('edit_user.html', user=user)

@app.route('/users/update/<int:id>', methods=['POST'])
@login_required
def update_user(id):
    username = request.form['username']
    conn = get_connection()

    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE id = %s",
                    (username, id)
                )
                conn.commit()
        finally:
            conn.close()
    return redirect(url_for('users'))

@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (username, encrypted_password) VALUES (%s, %s)",
                        (username, hashed_password)
                    )
                    conn.commit()
            finally:
                conn.close()
        return redirect(url_for('users'))

    return render_template('new_user.html')

@app.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    conn = get_connection()

    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (id,))
                conn.commit()
        finally:
            conn.close()

    return redirect(url_for('users'))

@app.route('/course_contents')
@login_required
def course_contents():
    conn = get_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM course_contents")
            course_contents = cursor.fetchall()
            conn.close()
    else:
        course_contents = []

    return render_template('course_contents.html', course_contents=course_contents)

@app.route('/create_course_content', methods=['GET', 'POST'])
@login_required
def create_course_content():
    if request.method == 'POST':
        type_of = request.form['type_of']
        language = request.form['language']
        lecture_title = request.form['lecture_title']
        lecture_no = request.form.get('lecture_no')
        youtube_link = request.form.get('youtube_link')
        ex_number = request.form.get('ex_number')
        ex_instruction = request.form.get('ex_instruction')

        conn = get_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO course_contents (type_of, language, lecture_title, lecture_no, youtube_link, ex_number, ex_instruction) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (type_of, language, lecture_title, lecture_no, youtube_link, ex_number, ex_instruction))
                conn.commit()
                conn.close()
            flash('Course content created successfully!', 'success')
        return redirect(url_for('course_contents'))

    return render_template('create_course_content.html')

@app.route('/edit_course_content/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course_content(id):
    conn = get_connection()
    course_content = None
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM course_contents WHERE id = %s", (id,))
            course_content = cursor.fetchone()
            conn.close()

    if request.method == 'POST':
        type_of = request.form['type_of']
        language = request.form['language']
        lecture_title = request.form['lecture_title']
        lecture_no = request.form.get('lecture_no')
        youtube_link = request.form.get('youtube_link')
        ex_number = request.form.get('ex_number')
        ex_instruction = request.form.get('ex_instruction')

        conn = get_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE course_contents 
                    SET type_of = %s, language = %s, lecture_title = %s, lecture_no = %s, youtube_link = %s, ex_number = %s, ex_instruction = %s 
                    WHERE id = %s
                """, (type_of, language, lecture_title, lecture_no, youtube_link, ex_number, ex_instruction, id))
                conn.commit()
                conn.close()
            flash('Course content updated successfully!', 'success')
        return redirect(url_for('course_contents'))

    return render_template('edit_course_content.html', course_content=course_content)

@app.route('/delete_course_content/<int:id>', methods=['POST'])
@login_required
def delete_course_content(id):
    conn = get_connection()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM course_contents WHERE id = %s", (id,))
            conn.commit()
            conn.close()
        flash('Course content deleted successfully!', 'success')
    return redirect(url_for('course_contents'))




@app.route('/process_selection', methods=['POST'])
@login_required
def process_selection():
    selected_ids = request.form.getlist('selected_courses')

    if not selected_ids:
        flash('No selections made. Please select at least one course content.')
        return redirect(url_for('course_contents'))

    conn = get_connection()
    if conn:
        try:
            selected_ids_str = ','.join(selected_ids)
            query = f"SELECT * FROM course_contents WHERE id IN ({selected_ids_str})"
            df = pd.read_sql_query(query, conn)
        finally:
            conn.close()

    num_reports = generate_reports(df)
    flash(f'{num_reports} reports generated successfully!')
    return redirect(url_for('course_contents'))


@app.route('/download/<file_name>')
def download_file(file_name):
    if file_exists(file_name):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_name, as_attachment=True)
    else:
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        if conn:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT id, username, encrypted_password, sign_in_count FROM users WHERE username = %s",
                        (username,))
                    user = cursor.fetchone()

                if user:
                    if check_password_hash(user['encrypted_password'], password):
                        user_obj = User(user['id'], user['username'])
                        login_user(user_obj)
                        session.permanent = True

                        with conn.cursor() as cursor:
                            cursor.execute(
                                "UPDATE users SET sign_in_count = sign_in_count + 1, last_sign_in_at = NOW() WHERE id = %s",
                                (user['id'],))
                            conn.commit()

                        return redirect(url_for('dashboard'))
                    else:
                        error_message = 'Incorrect password. Please try again.'
                else:
                    error_message = 'Username not found. Please try again.'
            except Exception as e:
                error_message = f"Database error: {str(e)}"
            finally:
                conn.close()
        else:
            error_message = 'Database connection error.'

    return render_template('login.html', error_message=error_message)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500

@app.before_request
def update_session_timeout():
    session.modified = True

if __name__ == "__main__":
    app.run(debug=True)
