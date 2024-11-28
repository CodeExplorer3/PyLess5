import sqlite3
import time
from bs4 import BeautifulSoup
import requests
import signal
import sys

# Constants
DATABASE = "weather.db"
TABLE_NAME = "weather_data"
URL = 'https://meteopost.com/city/5688/'

# Signal handler for stopping the program
def signal_handler(sig, frame):
    print("Program stopped.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create or connect to SQLite database
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            temperature REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Insert data into the database
def insert_data(temperature):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {TABLE_NAME} (date_time, temperature)
        VALUES (datetime('now', 'localtime'), ?)
    """, (temperature,))
    conn.commit()
    conn.close()

# Parse weather data from the website
def parse_weather():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            item_site = BeautifulSoup(response.text, features='html.parser')
            temperature_elements = item_site.find_all('span', {'class': 't'})
            for temp_element in temperature_elements:
                temperature = temp_element.text.strip().replace('°', '').replace('C', '').replace(',', '.')
                print(f"Temperature: {temperature}°C")
                break  # Only take the first temperature found
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Error parsing weather: {e}")

# Main loop for periodic updates
def main():
    create_database()
    print("Weather monitoring started. Press Ctrl+C to stop.")
    while True:
        parse_weather()
        time.sleep(1800)  # Wait for 30 minutes

if __name__ == "__main__":
    main()
