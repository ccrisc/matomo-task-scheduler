from db.db_connection import get_connection
import pytz
from datetime import datetime


# Log an API call
def log_api_call(status, status_code, total_rows_found, error_message):
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database for logging API call.")
        return

    cursor = conn.cursor()

    # SQL query to log API call details
    sql = """
    INSERT INTO api_calls (status_code, status, total_rows_found, error_message)
    VALUES (%s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (status_code, status, total_rows_found, error_message))
        conn.commit()
    except Exception as e:
        print(f"Failed to log API call: {e}")
    finally:
        cursor.close()
        conn.close()


def insert_data(data):
    """Insert idVisit and visitorId into the daily_visits table."""
    conn = get_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()

    # SQL query to insert idVisit and visitorId into daily_visits table
    sql_daily_visits = """
    INSERT INTO daily_visits (
        id_visit, visit_ip, visitor_id, user_id, visitor_type, visit_count, 
        visit_duration, number_of_actions, number_of_interactions, number_of_events, 
        device_type, device_brand, operating_system, device_model, browser_name, 
        country, latitude, longitude, seconds_since_first_visit, seconds_since_last_visit, 
        resolution, server_time
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (id_visit) DO NOTHING
    """

    # SQL query to insert data into action_details table
    sql_action_details = """
    INSERT INTO action_details (daily_visit_id, type, url, page_view_identifier, page_id_action, timestamp, page_view_position, title, subtitle, time_spent_seconds, page_load_time_milliseconds, event_category, event_action)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (page_view_identifier) DO NOTHING
    """

    try:
        for visit in data:
            id_visit = visit.get('idVisit')
            visit_ip = visit.get('visitIp')
            visitor_id = visit.get('visitorId')
            user_id = visit.get('userId')
            visitor_type = visit.get('visitorType')
            visit_count = visit.get('visitCount')
            visit_duration = visit.get('visitDuration')
            number_of_actions = visit.get('actions')
            number_of_interactions = visit.get('interactions')
            number_of_events = visit.get('events')
            device_type = visit.get('deviceType')
            device_brand = visit.get('deviceBrand')
            operating_system = visit.get('operatingSystem')
            device_model = visit.get('deviceModel')
            browser_name = visit.get('browserName')
            country = visit.get('country')
            latitude = visit.get('latitude')
            longitude = visit.get('longitude')
            seconds_since_first_visit = visit.get('secondsSinceFirstVisit')
            seconds_since_last_visit = visit.get('secondsSinceLastVisit')
            resolution = visit.get('resolution')
            server_timestamp = visit.get('serverTimestamp')
            server_time = datetime.utcfromtimestamp(server_timestamp).replace(tzinfo=pytz.UTC)

            # Ensure you have all the data you expect
            values = (
                id_visit, visit_ip, visitor_id, user_id, visitor_type, visit_count,
                visit_duration, number_of_actions, number_of_interactions, number_of_events,
                device_type, device_brand, operating_system, device_model, browser_name,
                country, latitude, longitude, seconds_since_first_visit, seconds_since_last_visit,
                resolution, server_time
            )

            # Insert data into daily_visits
            cursor.execute(sql_daily_visits, values)

            # Get the inserted visit ID (or the one already existing due to ON CONFLICT)
            cursor.execute("SELECT id FROM daily_visits WHERE id_visit = %s", (id_visit,))
            daily_visit_id = cursor.fetchone()[0]  # Assuming there is always a result

            # Insert data into action_details
            for action in visit.get('actionDetails', []):
                action_type = action.get('type')
                url = action.get('url')
                page_view_identifier = action.get('idpageview')
                page_id_action = action.get('pageIdAction')
                action_timestamp = action.get('timestamp')
                timestamp = datetime.utcfromtimestamp(action_timestamp).replace(tzinfo=pytz.UTC)
                page_view_position = action.get('pageviewPosition')
                title = action.get('title')
                subtitle = action.get('subtitle')
                time_spent_seconds = action.get('timeSpent')
                page_load_time_milliseconds = action.get('pageLoadTimeMilliseconds')
                event_category = action.get('eventCategory')
                event_action = action.get('eventAction')

                cursor.execute(sql_action_details, (
                    daily_visit_id, action_type, url, page_view_identifier, page_id_action, timestamp,
                    page_view_position, title, subtitle, time_spent_seconds, page_load_time_milliseconds,
                    event_category, event_action))

        conn.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        cursor.close()
        conn.close()