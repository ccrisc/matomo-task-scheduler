from main import fetch_data
from db.db_connection import get_connection
import os
from dotenv import load_dotenv

load_dotenv()


def test_api_call():
    """Test the fetch_data function by calling the API and inserting the result into the database."""
    url = os.getenv('MATOMO_API_URL')  # Fetch the URL from environment variables

    # Fetch data using the fetch_data function
    print("Testing API call...")

    # Check connection details
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT current_database();")
        print("Connected to database:", cursor.fetchone()[0])
        cursor.close()
        conn.close()

    # Call the fetch_data function and capture the result
    result = fetch_data(url)

    # Check if the result is valid or None (in case of failure)
    if result:
        print("API Call Success!")
        print("Fetched Data:", result)  # Print the data fetched

        # Insert data into the database
        from db.insert_data import insert_data  # Replace 'your_module' with the actual module name
        insert_data(result)  # Call insert_data function with the fetched data
    else:
        print("API Call Failed")


if __name__ == "__main__":
    test_api_call()
