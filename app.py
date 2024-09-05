from flask import Flask
import psycopg2
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests

DATABASE_URL = os.getenv('DATABASE_URL', 'your-supabase-db-url')

def fetch_api_data():
    # Your API call logic here
    response = requests.get('https://api.example.com/data')
    data = response.json()

    # Connect to Supabase and insert data
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO your_table (column) VALUES (%s)', (data['field'],))
    conn.commit()
    cur.close()
    conn.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_api_data, 'interval', days=1)
    scheduler.start()

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask app running!'



if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True)