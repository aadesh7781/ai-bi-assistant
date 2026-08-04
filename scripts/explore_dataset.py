from pathlib import Path
import pandas as pd

csv_file = Path("spotify_2015_2025_85k.csv")

df = pd.read_csv(csv_file)

print("\n========== FIRST 5 ROWS ==========\n")
print(df.head())

print("\n========== SHAPE ==========\n")
print(df.shape)

print("\n========== COLUMNS ==========\n")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========\n")
print(df.dtypes)

print("\n========== MISSING VALUES ==========\n")
print(df.isnull().sum())