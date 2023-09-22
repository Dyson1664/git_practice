import requests
import json
import sqlite3

# 1. Set up the SQLite Database and Table
def setup_database():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS WEATHER (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CITY TEXT,
            TIME TEXT,
            TEMPERATURE REAL
        );
    """)
    conn.commit()
    conn.close()

setup_database()

# Function to insert data into the SQLite database
def insert_into_database(city, time, temperature):
    conn = sqlite3.connect("weather_data.db")
    with conn:
        conn.execute("INSERT INTO WEATHER (CITY, TIME, TEMPERATURE) VALUES (?, ?, ?)", (city, time, temperature))

# Define the API endpoint
api_url = "https://api.open-meteo.com/v1/forecast"

# List of locations with their latitude and longitude
locations = [
    {"name": "New York City",
     "latitude": 40.7128,
     "longitude": -74.0060},
    {"name": "Dublin", "latitude": 53.3331, "longitude": -6.2489},
    {"name": "Hanoi", "latitude": 21.0245, "longitude": 105.8412},
    # ... add more locations as needed
]
for location in locations:
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": "temperature_2m"
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        weather_data = json.loads(response.text)
        time = weather_data['hourly']['time'][0]
        temperature = weather_data['hourly']['temperature_2m'][0]

        # Insert the data into the database
        insert_into_database(location['name'], time, temperature)


# 3. Query the Database
def query_all_data():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT CITY, TIME, TEMPERATURE FROM WEATHER")
    for row in cursor.fetchall():
        print(f"City: {row[0]}, Time: {row[1]}, Temperature: {row[2]}°C")
    conn.close()


query_all_data()