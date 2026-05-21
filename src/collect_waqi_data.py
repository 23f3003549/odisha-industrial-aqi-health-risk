import requests
import pandas as pd
from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.config import WAQI_CITIES, DATA_PATH , WAQI_API_KEY , OPENWEATHER_API_KEY



def get_aqi_data(city):
    """Fetch current AQI data for a city"""
    url = f"https://api.waqi.info/feed/{city}/?token={WAQI_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        # import json
        # print(json.dumps(data, indent=4))
        
        
        if data["status"] == "ok":
            aqi_data = data["data"]
            
            result = {
                "city": city,
                "timestamp": aqi_data["time"]["iso"],
                "aqi": aqi_data.get("aqi", None),
                "pm25": aqi_data["iaqi"].get("pm25", {}).get("v", None),
                "pm10": aqi_data["iaqi"].get("pm10", {}).get("v", None),
                "no2": aqi_data["iaqi"].get("no2", {}).get("v", None),
                "so2": aqi_data["iaqi"].get("so2", {}).get("v", None),
                "co": aqi_data["iaqi"].get("co", {}).get("v", None),
                "o3": aqi_data["iaqi"].get("o3", {}).get("v", None),
                "dew": aqi_data["iaqi"].get("dew", {}).get("v", None),
                "temperature": aqi_data["iaqi"].get("t", {}).get("v", None),
                "humidity": aqi_data["iaqi"].get("h", {}).get("v", None),
                "wind": aqi_data["iaqi"].get("w", {}).get("v", None),
            }
            return result
        else:
            print(f"Error fetching {city}: {data['status']}")
            return None
            
    except Exception as e:
        print(f"Exception for {city}: {e}")
        return None
   


def collect_all_cities():
    """Collect AQI data for all cities and save to CSV"""
    all_data = []
    
    for city , stations in WAQI_CITIES.items():
        for station in stations:
            print(f"Fetching data for {station}...")
            data = get_aqi_data(station)
            
            if data:
               all_data.append(data)
               print(f"{station} -> AQI: {data['aqi']}")
            else:
                print(f"{station} -> No data found")
    
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Save to CSV
        os.makedirs(DATA_PATH, exist_ok=True)
        filename = os.path.join(DATA_PATH, f"waqi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
        print(df)
        return df
    else:
        print("No data collected")
        return None
    



