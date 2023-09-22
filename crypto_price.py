import requests
from dotenv import load_dotenv
import os
import json
import sqlite3

# Load .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("API_KEY")

def fetch_latest_crypto_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    target_ids = [1, 1027, 5426]
    parameters = {
        'id': ','.join(map(str, target_ids)),
    }

    response = requests.get(url, headers=headers, params=parameters)

    if response.status_code == 200:
        data = json.loads(response.text)
        crypto_data = data['data']

        for target_id in target_ids:
            if str(target_id) in crypto_data:
                value = crypto_data[str(target_id)]
                print(
                    f"{value['name']}, {value['symbol']}, USD Price - ${round(value['quote']['USD']['price'], 2)}, Max supply: {value['max_supply']}, Circulating supply: {value['circulating_supply']}")

        return crypto_data  # Return data if status code is 200
    else:
        print(f"Failed to retrieve data: {response.content}")
        return None  # Return None if status code is not 200

def create_database():
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CRYPTO (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CRYPTO_ID INTEGER,
            NAME TEXT,
            SYMBOL TEXT,
            USD_PRICE REAL,
            MAX_SUPPLY REAL,
            CIRCULATING_SUPPLY REAL
        );
    """)
    conn.commit()
    print("Table created successfully.")
    return conn

def insert_into_database(conn, crypto_data):
    cursor = conn.cursor()
    for crypto_id, data in crypto_data.items():
        cursor.execute(
            "INSERT INTO CRYPTO (CRYPTO_ID, NAME, SYMBOL, USD_PRICE, MAX_SUPPLY, CIRCULATING_SUPPLY) VALUES (?, ?, ?, ?, ?, ?)",
            (crypto_id, data['name'], data['symbol'], data['quote']['USD']['price'], data['max_supply'], data['circulating_supply']))
    conn.commit()
    print("Data inserted successfully.")

def query_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CRYPTO")
    for row in cursor.fetchall():
        print(row[2], round(row[4], 2))

if __name__ == "__main__":
    if api_key:
        print(f"Successfully loaded API key: {api_key}\n")
        conn = create_database()
        crypto_data = fetch_latest_crypto_data()
        if crypto_data:
            insert_into_database(conn, crypto_data)
            query_all_data(conn)
        conn.close()
    else:
        print("Failed to load API key.")



