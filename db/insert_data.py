from db.db_connection import get_connection

# Log an API call
def log_api_call(status, status_code, total_rows_found, error_message):
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database for logging API call.")
        return

    cursor = conn.cursor()

    # SQL query to log API call details
    sql = """
    INSERT INTO api_calls (status, status_code, total_rows_found, error_message)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (status, status_code, total_rows_found, error_message))
        conn.commit()
    except Exception as e:
        print(f"Failed to log API call: {e}")
    finally:
        cursor.close()
        conn.close()

def insert_data(data):
    """Insert the fetched data into the database."""
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # SQL query to insert data into daily_visits table
    sql = """
    INSERT INTO daily_visits (idVisit, visitIp)
    VALUES (%s, %s)
    ON CONFLICT (idVisit) DO NOTHING
    """

    for visit in data:
        id_visit = visit.get('idVisit')
        visit_ip = visit.get('visitIp')
        if id_visit and visit_ip:
            cursor.execute(sql, (id_visit, visit_ip))

    conn.commit()
    cursor.close()
    conn.close()