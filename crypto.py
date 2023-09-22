import requests
from dotenv import load_dotenv
import os
import json

# Load .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")

if api_key:
    print(f"Successfully loaded API key: {api_key}")
else:
    print("Failed to load API key.")

def fetch_latest_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    parameters = {
        'start': '1',
        'limit': '10',
        'symbol': 'BTC,ETH,SOL',


    }

    response = requests.get(url, headers=headers, params=parameters)

    if response.status_code == 200:
        data = json.loads(response.text)
        try:
            bitcoin_data = next(item for item in data['data'] if item['symbol'] == 'BTC')
            print(f"Bitcoin Data: {bitcoin_data}")
            print(bitcoin_data['rank'])
            print(bitcoin_data['name'])
            print('0')
            return data
        except (KeyError, StopIteration):
            print("Bitcoin data not found in response.")
            return None
    else:
        print(f"Failed to retrieve data: {response.content}")
        return None

if __name__ == "__main__":
    data = fetch_latest_crypto_data()
    if data:
        print(data)
        for name in data['data']:
            if name['name'] == 'Bitcoin':
                print(f"Name is: {name['name']}")
                print(f"Symbol: {name['symbol']}")
                print(f"First_historical_data is: {name['first_historical_data']}")


