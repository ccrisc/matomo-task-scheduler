import requests
import os
from db.insert_data import insert_data, log_api_call

# Load environment variables if in development
if os.getenv('ENVIRONMENT') == 'development':
    from dotenv import load_dotenv

    load_dotenv()

API_URL = os.getenv('MATOMO_API_URL')


# Fetch data from the API, handle errors, and log the call into db.
def fetch_data(url):
    try:
        response = requests.get(url)
        # Raise an exception for HTTP error responses
        response.raise_for_status()

        data = response.json()

        # Check if the data is a list
        if isinstance(data, list):
            total_rows = len(data)
        else:
            total_rows = 0

        # Log successful API call with no error message
        log_api_call(status="success", status_code=response.status_code, total_rows_found=total_rows,
                     error_message=None)

    except requests.RequestException as e:
        log_api_call(status="failure", status_code=getattr(e.response, 'status_code', 'N/A'), total_rows_found=0,
                     error_message=str(e))
        return None

    except ValueError as e:
        log_api_call(status="failure", status_code=response.status_code if 'response' in locals() else 'N/A',
                     total_rows_found=0, error_message=f"JSON decoding failed: {e}")
        return None


def main():
    """Main function to fetch data and insert it into the database."""
    data = fetch_data(API_URL)

    if data:
        insert_data(data)  # Insert data into the database if fetching was successful
    else:
        print("No data to insert into the database.")


if __name__ == "__main__":
    main()
