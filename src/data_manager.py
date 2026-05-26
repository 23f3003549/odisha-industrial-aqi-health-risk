import pandas as pd
import os
import glob
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs.config import DATA_PATH

def merge_all_snapshots(source="owm"):
    """Merge all snapshot CSVs into one master file"""
    
    # Find all files for this source
    pattern = os.path.join(DATA_PATH, f"{source}_data_*.csv")
    files = glob.glob(pattern)
    
    if not files:
        print(f"No {source} files found")
        return None
    
    print(f"Found {len(files)} {source} snapshots...")
    
    # Merge all into one
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Sort by city and timestamp
    df = df.sort_values(["city", "timestamp"]).reset_index(drop=True)
    
    # Save master file
    master_path = os.path.join("data/processed/", f"{source}_master.csv")
    os.makedirs("data/processed/", exist_ok=True)
    df.to_csv(master_path, index=False)
    
    print(f"Master file saved: {master_path}")
    print(f"Total records: {len(df)}")
    return df



# ── PATH CONFIG ───────────────────────────────────────────

RAW_HISTORICAL = 'data/raw/historical_data/'
PROCESSED      = 'data/processed/'

HISTORICAL_FILES = {
    'talcher':      os.path.join(RAW_HISTORICAL, 'talcher_historical.csv'),
    'jharsuguda': os.path.join(RAW_HISTORICAL, 'brajrajnagar_historical.csv')
}

LIVE_FILES = {
    'waqi': os.path.join(PROCESSED, 'waqi_master.csv'),
    'owm':  os.path.join(PROCESSED, 'owm_master.csv')
}

OUTPUT_FILES = {
    'historical_master': os.path.join(PROCESSED, 'waqi_historical_master.csv'),
    'master_full':       os.path.join(PROCESSED, 'master_full.csv')
}

# ── STEP 1: CLEAN + MERGE HISTORICAL ─────────────────────

def load_historical():
    """
    Reads talcher + brajrajnagar historical CSVs
    Cleans and merges into one file
    Saves → processed/waqi_historical_master.csv
    """
    all_cities = []

    for city, filepath in HISTORICAL_FILES.items():

        if not os.path.exists(filepath):
            print(f"⚠️  Not found: {filepath} — skipping")
            continue

        df = pd.read_csv(filepath)
        print(f"\n📂 {city} raw columns: {df.columns.tolist()}")
        print(f"   Shape: {df.shape}")

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower()

        # Rename date column
        for col in ['datetime', 'timestamp', 'time', 'date']:
            if col in df.columns:
                df.rename(columns={col: 'date'}, inplace=True)
                break

        # Rename pm25 variations
        for col in ['pm2.5', 'pm2_5']:
            if col in df.columns:
                df.rename(columns={col: 'pm25'}, inplace=True)
                break

        # Parse date
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

        # Add city
        df['city'] = city

        # Keep only pollutant columns
        cols = ['city', 'date', 'pm25', 'pm10', 'o3', 'no2', 'so2', 'co']
        cols = [c for c in cols if c in df.columns]
        df = df[cols]

        # Remove invalid values
        for col in ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].apply(lambda x: x if pd.notna(x) and x >= 0 else None)

        # Drop missing dates
        df = df.dropna(subset=['date'])
        df = df.sort_values('date').reset_index(drop=True)

        print(f"   ✅ Cleaned: {df.shape}")
        print(f"   📅 Range: {df['date'].min()} → {df['date'].max()}")

        all_cities.append(df)

    if not all_cities:
        print("❌ No historical files found!")
        return None

    # Merge both cities
    historical_master = pd.concat(all_cities, ignore_index=True)
    historical_master = historical_master.sort_values(['city', 'date']).reset_index(drop=True)

    # Save
    historical_master.to_csv(OUTPUT_FILES['historical_master'], index=False)
    print(f"\n✅ Historical master saved → {OUTPUT_FILES['historical_master']}")
    print(f"   Total rows: {len(historical_master)}")
    print(f"   Missing:\n{historical_master.isnull().sum()}")

    return historical_master


# ── STEP 2: LOAD + CLEAN LIVE DATA ───────────────────────

def load_live():
    # Load
    waqi = pd.read_csv(LIVE_FILES['waqi'])
    owm  = pd.read_csv(LIVE_FILES['owm'])

    # Standardize column names
    waqi.columns = waqi.columns.str.strip().str.lower()
    owm.columns  = owm.columns.str.strip().str.lower()

    # Rename timestamp → date
    waqi.rename(columns={'timestamp': 'date'}, inplace=True)
    owm.rename(columns={'timestamp':  'date'}, inplace=True)

    # Rename pm2_5 → pm25 in OWM
    owm.rename(columns={
        'pm2_5':      'pm25',
        'wind_speed': 'wind'
    }, inplace=True)

    # ── FIX 1: Standardize WAQI city names ──────────────
    # Map full WAQI station names → simple city names
    city_mapping = {
        'talcher coalfields, talcher, india': 'talcher',
        ' gm office, brajrajnagar, india':    'jharsuguda',
        'gm office, brajrajnagar, india':     'jharsuguda',
    }

    waqi['city'] = waqi['city'].str.strip().str.lower().map(city_mapping)

    # Drop rows where city mapping failed
    unmapped = waqi[waqi['city'].isna()]
    if len(unmapped) > 0:
        print(f"⚠️  Unmapped WAQI cities: {unmapped['city'].unique()}")
    waqi = waqi.dropna(subset=['city'])

    # Standardize OWM city names too
    owm['city'] = owm['city'].str.strip().str.lower()

    print(f"\n   WAQI cities after mapping: {waqi['city'].unique()}")
    print(f"   OWM  cities: {owm['city'].unique()}")

    # ── FIX 2: Parse + normalize timestamps ─────────────
    waqi['date'] = pd.to_datetime(waqi['date'], utc=True).dt.tz_convert(None)
    owm['date']  = pd.to_datetime(owm['date'],  utc=False)

    # Round both to nearest hour
    waqi['date'] = waqi['date'].dt.round('h')
    owm['date']  = owm['date'].dt.round('h')

    print(f"\n   WAQI sample dates: {waqi['date'].head(3).tolist()}")
    print(f"   OWM  sample dates: {owm['date'].head(3).tolist()}")

    # ── OWM extra columns only ───────────────────────────
    owm_extra_cols = [
        'city', 'date',
        'no', 'nh3',
        'wind_direction', 'pressure',
        'feels_like',
        'weather', 'weather_description'
    ]
    owm_extra_cols = [c for c in owm_extra_cols if c in owm.columns]

    # ── Merge ────────────────────────────────────────────
    live_merged = pd.merge(
        waqi,
        owm[owm_extra_cols],
        on=['city', 'date'],
        how='left'  # left join — keep all WAQI rows even if OWM doesn't match
    )

    print(f"\n✅ Live merged shape: {live_merged.shape}")
    print(f"   Cities in merge: {live_merged['city'].unique()}")
    print(f"   Date range: {live_merged['date'].min()} → {live_merged['date'].max()}")

    return live_merged


# ── STEP 3: ADD TIME FEATURES ─────────────────────────────

def add_time_features(df):
    """Adds hour, day, month, season, weekend flag"""

    df['hour']        = df['date'].dt.hour
    df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday
    df['month']       = df['date'].dt.month
    df['is_weekend']  = df['day_of_week'].isin([5, 6]).astype(int)
    df['season']      = df['month'].map({
        12: 'winter', 1: 'winter',  2: 'winter',
        3:  'spring', 4: 'spring',  5: 'spring',
        6:  'summer', 7: 'summer',  8: 'summer',
        9:  'monsoon',10: 'monsoon',11: 'monsoon'
    })

    return df


# ── STEP 4: FINAL MERGE ───────────────────────────────────

def build_master_full():
    """
    Combines historical + live data
    Adds time features
    Saves → processed/master_full.csv
    This is your FINAL file for EDA + modeling
    """

    # Load historical master
    if not os.path.exists(OUTPUT_FILES['historical_master']):
        print("Historical master not found — running load_historical() first...")
        historical = load_historical()
    else:
        historical = pd.read_csv(OUTPUT_FILES['historical_master'])
        historical['date'] = pd.to_datetime(historical['date'])

    # Load live merged
    live = load_live()

    # Add time features to both
    historical = add_time_features(historical)
    live       = add_time_features(live)

    # Combine historical + live
    # Historical has only pollutants, live has pollutants + weather
    master_full = pd.concat([historical, live], ignore_index=True)

    # Sort + drop duplicates
    master_full = master_full.sort_values(['city', 'date'])
    master_full = master_full.drop_duplicates(subset=['city', 'date'])
    master_full = master_full.reset_index(drop=True)

    # Save
    master_full.to_csv(OUTPUT_FILES['master_full'], index=False)

    print(f"\n✅ master_full.csv saved → {OUTPUT_FILES['master_full']}")
    print(f"   Total rows : {len(master_full)}")
    print(f"   Columns    : {master_full.columns.tolist()}")
    print(f"   Date range : {master_full['date'].min()} → {master_full['date'].max()}")
    print(f"   Cities     : {master_full['city'].unique()}")
    print(f"\n   Missing values:")
    print(master_full.isnull().sum())

    return master_full


# ── RUN ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("Merging snapshots")

    merge_all_snapshots("owm")
    merge_all_snapshots("waqi")


    print("=" * 50)
    print("STEP 1 — Merging historical files...")
    print("=" * 50)
    load_historical()

    print("\n" + "=" * 50)
    print("STEP 2 — Building master_full.csv...")
    print("=" * 50)
    build_master_full()

    print("\n🎉 data_manager.py complete!")   