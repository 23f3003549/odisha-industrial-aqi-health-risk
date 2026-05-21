from dotenv import load_dotenv
import os
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY").strip()
WAQI_API_KEY = os.getenv("WAQI_API_KEY")

print("OPENWEATHER:", OPENWEATHER_API_KEY)
print("WAQI:", WAQI_API_KEY)

WAQI_CITIES =  {
    "talcher": ["Talcher Coalfields, Talcher, India"],
    "angul" : ["Hakimapada, Angul, India"],
    "jharsuguda" : [" GM Office, Brajrajnagar, India"],
    "rourkela": [
        "Sector-2, Rourkela, India",
        "Raghunathpali, Rourkela, India",
        "Fertilizer Township, Rourkela, India"
    ],
    "sundargarh" : ["Barsua Iron Ore Mines, Tensa, Koida, India"],
    "kendujhar" : [
        "OMC Colony, Suakati, Kendujhar Sadar, India",
        "Jagamohanpur, Keonjhar, Kendujhargarh, India"
    ],
    "baripada": ["Meher Colony, Baripada, India"]
}

CITIES = {
    "talcher": (20.95, 85.23),
    "angul": (20.84, 85.10),
    "jharsuguda": (21.85, 84.01),
    "rourkela": (22.26, 84.85),
    "sundargarh": (22.12, 84.03),
    "kendujhar": (21.63, 85.58),
    "baripada": (21.93, 86.73)
}

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(BASE_PATH, "data", "processed")
API_TIMEOUT = 10

#AQI Health risk thresholds

AQI_THRESHOLDS = {
    (0,50) :"Good",
    (51,100): "Satisfactory",
    (101,200) : "Moderate",
    (201,300) : "Poor",
    (301,400) : "Very Poor",
    (401,500) : "Severe"
}