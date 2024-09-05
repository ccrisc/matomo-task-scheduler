# api/main.py
import requests
import os
from db.insert_data import insert_data, log_api_call

API_URL = os.getenv('API_URL')

def fetch_data(url):
    """Fetch data from the API, handle errors, and log the call."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        total_rows = len(data.get('visits', []))  # Assuming 'visits' contains the data rows

        # Log successful API call
        log_api_call(status="success", status_code=response.status_code, total_rows_found=total_rows)

        return data

    except requests.RequestException as e:
        # Log failed API call with the status code and error message
        log_api_call(status="failure", status_code=getattr(e.response, 'status_code', 'N/A'), total_rows_found=0, error_message=str(e))
        print(f"API Request failed: {e}")
        return None

    except ValueError as ve:
        # Log failed API call due to JSON decoding issues
        log_api_call(status="failure", status_code=response.status_code, total_rows_found=0, error_message=f"JSON decoding failed: {ve}")
        print(f"API Response decoding failed: {ve}")
        return None

def main():
    """Main function to fetch data and insert it into the database."""
    data = fetch_data(API_URL)

    if data:
        # Insert data into the database if fetching was successful
        insert_data(data)
    else:
        print("No data to insert into the database.")

if __name__ == "__main__":
    main()
