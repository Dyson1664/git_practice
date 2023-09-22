import requests

def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': 21.028511,
        'longitude': 105.804817,
        'hourly': 'temperature_2m,windspeed_10m,visibility',
        'daily': 'precipitation_sum'# Include windspeed_10m
          # This is to specify the unit of the windspeed
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['hourly'].get('temperature_2m', [None])[0]
        wind_speed = data['hourly'].get('windspeed_10m', [None])[0]
        rain = data['daily'].get('precipitation_sum', [None])[0]
        visabil = data['hourly'].get('visibility', [None])[0]
        return {
            'latitude': params['latitude'],
            'longitude': params['longitude'],
            'temperature': temperature,
            'windspeed': wind_speed,
            'rainfall': rain,
            'visibility': visabil
        }
    else:
        print(f"Failed to get data: {response.content}")
        return None


import sqlite3

def setup_database():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            temperature REAL, 
            windspeed REAL,
            rainfall REAL,
            visibility REAL
        );
    """)
    conn.commit()
    conn.close()


def insert_into_database(data):
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO forecasts (latitude, longitude, temperature, windspeed, rainfall, visibility) VALUES (?, ?, ?, ?, ?, ?)",
                   (data['latitude'], data['longitude'], data['temperature'], data['windspeed'], data['rainfall'], data['visibility']))
    conn.commit()
    conn.close()


def fetch_from_database():
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forecasts")
    rows = cursor.fetchall()
    conn.close()
    return rows



if __name__ == "__main__":
    setup_database()
    data = fetch_weather_data()
    if data:
        insert_into_database(data)
    # Fetch and print all rows from the database to confirm the data was inserted
    print(fetch_from_database())

rows2 = fetch_from_database()

for row in rows2:
    print(f"ID: {row[0]}, Latitude: {row[1]}, Longitude: {row[2]}, Temperature: {row[3]}, Windspeed: {row[4]}, Rainfall: {row[5]}, Visability: {row[6]}")
