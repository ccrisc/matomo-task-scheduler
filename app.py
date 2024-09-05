from flask import Flask
import os
import requests
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
