import pandas as pd
import sqlite3
import os

downloads = r"C:/Users/Administrator/Downloads"

# ----------- EMBEDDED GITHUB RAW INPUT (WORKING) -----------
InputFileURL = "https://raw.githubusercontent.com/chriswmann/datasets/master/500_Person_Gender_Height_Weight_Index.csv"

# Input warehouse DB
dw = os.path.join(downloads, "datawarehouse.db")
conn_dw = sqlite3.connect(dw)

# Load GitHub CSV into Data Warehouse
df_raw = pd.read_csv(InputFileURL)

# Prepare columns exactly as required for Dim-BMI
df_raw["PersonID"] = df_raw.index + 1
df_raw["Height"] = df_raw["Height"] / 100  # convert cm → meters
df_raw["bmi"] = df_raw["Weight"] / (df_raw["Height"] ** 2)
df_raw["Indicator"] = df_raw["Index"]

df_raw = df_raw[["PersonID", "Height", "Weight", "bmi", "Indicator"]]

df_raw.to_sql("Dim-BMI", conn_dw, if_exists="replace", index=False)
# ----------------------------------------------------------

# Output datamart DB
dm = os.path.join(downloads, "datamart.db")
conn_dm = sqlite3.connect(dm)

# Load full table
df = pd.read_sql("SELECT * FROM [Dim-BMI]", conn_dw)

# Island-style slicing → rows + columns
island = df[df["Indicator"] > 2][["Height", "Weight", "Indicator"]]

# Save into datamart
island.to_sql("Dim-BMI-Island", conn_dm, if_exists="replace", index=False)

# Print summary
print("Full dataset:", df.shape)
print("Island sliced dataset:", island.shape)
