import psycopg2
import os


# Connect to DB
def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('SUPABASE_HOST'),
            port=os.getenv('SUPABASE_PORT'),
            dbname=os.getenv('SUPABASE_DB_NAME'),
            user=os.getenv('SUPABASE_USER'),
            password=os.getenv('SUPABASE_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

# generate new user password
# from werkzeug.security import generate_password_hash
# password = "12345678"
# hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
# print(f"Hashed Password: {hashed_password}")
