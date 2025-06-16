import requests
import time
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API URL
url = "https://api.data.gov.my/data-catalogue?id=fuelprice"


# Function to fetch data with retries and error handling
def fetch_fuel_price_data(url, retries=3, wait_time=2):
    attempt = 0
    while attempt < retries:
        try:
            logging.info(f"Attempt {attempt + 1} - Requesting data...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
            data = response.json()  # May raise ValueError if response is not JSON
            logging.info("Data successfully retrieved!")
            return data
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error: {req_err}")
        except ValueError as json_err:
            logging.error(f"JSON decode error: {json_err}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

        attempt += 1
        logging.info(f"Retrying in {wait_time} seconds...")
        time.sleep(wait_time)

    logging.error("All retry attempts failed.")
    return None


# Run the function and show a sample of the data
if __name__ == "__main__":
    fuel_data = fetch_fuel_price_data(url)
    if fuel_data:
        print("Sample Data:")
        print(fuel_data[0] if isinstance(fuel_data, list) and len(fuel_data) > 0 else fuel_data)
    else:
        print("Failed to retrieve data after retries.")
