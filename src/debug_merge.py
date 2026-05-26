import pandas as pd
import os

waqi = pd.read_csv('data/processed/waqi_master.csv')
owm  = pd.read_csv('data/processed/owm_master.csv')

print("=== WAQI ===")
print(f"Columns: {waqi.columns.tolist()}")
print(f"Shape: {waqi.shape}")
print(f"Sample timestamps:\n{waqi['timestamp'].head(5).tolist()}")
print(f"Cities: {waqi['city'].unique()}")

print("\n=== OWM ===")
print(f"Columns: {owm.columns.tolist()}")
print(f"Shape: {owm.shape}")
print(f"Sample timestamps:\n{owm['timestamp'].head(5).tolist()}")
print(f"Cities: {owm['city'].unique()}")