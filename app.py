# app.py
from flask import Flask, render_template, request
from db.db_connection import get_connection

app = Flask(__name__)


# Helper function to fetch filtered data from `api_calls` table
def fetch_api_calls(date=None, status=None):
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor()

    # Base SQL query to fetch data
    sql = "SELECT timestamp, status, status_code, total_rows_found, error_message FROM api_calls WHERE 1=1"

    params = []

    # Add filtering conditions if provided
    if date:
        sql += " AND timestamp::date = %s"
        params.append(date)

    if status:
        sql += " AND status = %s"
        params.append(status)

    sql += " ORDER BY timestamp DESC"

    cursor.execute(sql, params)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


# Route to display and filter API calls
@app.route('/api-calls')
def api_calls():
    # Get filter parameters from URL
    date_filter = request.args.get('date')  # Expecting a date in 'YYYY-MM-DD' format
    status_filter = request.args.get('status')  # Expecting 'success' or 'failure'

    # Fetch filtered data
    calls = fetch_api_calls(date=date_filter, status=status_filter)

    return render_template('api_calls.html', calls=calls, date_filter=date_filter, status_filter=status_filter)


if __name__ == "__main__":
    app.run(debug=True)
