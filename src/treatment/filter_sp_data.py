import pandas as pd
from pathlib import Path

# Get the directory of the current script
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
input_file = ROOT_DIR / "data" / "processed" / "city_business_gee.csv"
output_file = ROOT_DIR / "data" / "processed" / "sao_paulo_data.csv"

print(f"Reading {input_file}...")
if not input_file.exists():
    print(f"Error: {input_file} not found!")
    exit(1)

df = pd.read_csv(input_file)

print("Filtering for Sao Paulo state...")
sp_data = df[df["state_name"] == "Sao Paulo"]

print(f"Saving to {output_file}...")
sp_data.to_csv(output_file, index=False)

print(f"Done! Filtered {len(sp_data)} rows. Saved to {output_file}.")
