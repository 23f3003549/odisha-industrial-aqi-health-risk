import requests
import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.config import CITIES, DATA_PATH , OPENWEATHER_API_KEY

def get_aqi_data(city, lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution?"
        f"lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        if "list" in data:

            pollution = data["list"][0]

            components = pollution["components"]

            result = {
                "city": city,
                "timestamp": datetime.now(),

                # AQI scale 1-5
                "aqi": pollution["main"]["aqi"],

                "co": components.get("co"),
                "no": components.get("no"),
                "no2": components.get("no2"),
                "o3": components.get("o3"),
                "so2": components.get("so2"),
                "pm2_5": components.get("pm2_5"),
                "pm10": components.get("pm10"),
                "nh3": components.get("nh3")
            }

            return result

        else:
            print(f"No data for {city}")
            print(data)
            return None

    except Exception as e:
        print(f"Error for {city}: {e}")
        return None


def collect_all_cities():

    all_data = []

    for city, coords in CITIES.items():

        lat, lon = coords

        print(f"Fetching AQI for {city}...")

        data = get_aqi_data(city, lat, lon)

        if data:
            all_data.append(data)
            print(f"{city} -> AQI: {data['aqi']}")

    if all_data:

        df = pd.DataFrame(all_data)

        os.makedirs(DATA_PATH, exist_ok=True)

        filename = os.path.join(
            DATA_PATH,
            f"owm_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        df.to_csv(filename, index=False)

        print(f"\nSaved to: {filename}")

        print(df)

        return df

    else:
        print("No data collected")
        return None

   


if __name__ == "__main__":
    collect_all_cities()
