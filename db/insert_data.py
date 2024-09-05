# db/insert_queries.py
from db.db_connection import get_connection


def insert_data(data):
    """Insert the fetched data into the database."""
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # Example of inserting data, you need to modify this according to your actual data structure.
    sql = """
    INSERT INTO visits (idSite, idVisit, visitIp, visitorId, fingerprint, url, pageTitle, serverTimePretty, timeSpent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (idVisit) DO NOTHING
    """

    for visit in data.get('visits', []):
        cursor.execute(sql, (
            visit.get('idSite'), visit.get('idVisit'), visit.get('visitIp'), visit.get('visitorId'),
            visit.get('fingerprint'), visit['actionDetails'][0].get('url'),
            visit['actionDetails'][0].get('pageTitle'), visit['actionDetails'][0].get('serverTimePretty'),
            visit['actionDetails'][0].get('timeSpent')
        ))

    conn.commit()
    cursor.close()
    conn.close()


def log_api_call(status, status_code, total_rows_found, error_message=None):
    """Log an API call with its status, status code, total rows found, and any error message."""
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
