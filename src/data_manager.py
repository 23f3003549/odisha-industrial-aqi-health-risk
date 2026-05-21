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

if __name__ == "__main__":
    merge_all_snapshots("owm")
    merge_all_snapshots("waqi")