import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collect_owm_data import collect_all_cities as collect_owm
from collect_waqi_data import collect_all_cities as collect_waqi

if __name__ == "__main__":
    print("=" * 50)
    print("Collecting OWM data...")
    print("=" * 50)
    owm_df = collect_owm()

    print("\n" + "=" * 50)
    print("Collecting WAQI data...")
    print("=" * 50)
    waqi_df = collect_waqi()

    print("\nDone.Both sources collected successfully.")