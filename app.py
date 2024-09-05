from flask import Flask, render_template
from db.db_connection import get_connection
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api_calls')
def api_calls():
    conn = get_connection()
    if conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM api_calls ORDER BY id DESC")
            api_calls = cursor.fetchall()
            cursor.close()
            conn.close()
    else:
        api_calls = []

    return render_template('api_calls.html', api_calls=api_calls)


if __name__ == "__main__":
    app.run(debug=True)
