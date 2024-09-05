import psycopg2
import os


# Connect to DB
def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('SUPABASE_HOST'),
            port=os.getenv('SUPABASE_PORT'),
            dbname=os.getenv('SUPABASE_DB'),
            user=os.getenv('SUPABASE_USER'),
            password=os.getenv('SUPABASE_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None
