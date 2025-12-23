import pandas as pd
import sqlite3
import os

downloads = r"C:/Users/Administrator/Downloads"

# ----------- EMBEDDED GITHUB RAW INPUT (WORKING) -----------
InputFileURL = "https://raw.githubusercontent.com/chriswmann/datasets/master/500_Person_Gender_Height_Weight_Index.csv"

# Input: Data Warehouse
dw = os.path.join(downloads, "datawarehouse.db")
conn_dw = sqlite3.connect(dw)

# Load GitHub CSV into Data Warehouse (ETL step)
df_raw = pd.read_csv(InputFileURL)

# Prepare columns exactly as required for Dim-BMI
df_raw["PersonID"] = df_raw.index + 1
df_raw["Height"] = df_raw["Height"] / 100  # convert cm → meters
df_raw["bmi"] = df_raw["Weight"] / (df_raw["Height"] ** 2)
df_raw["Indicator"] = df_raw["Index"]

df_raw = df_raw[["PersonID", "Height", "Weight", "bmi", "Indicator"]]

df_raw.to_sql("Dim-BMI", conn_dw, if_exists="replace", index=False)
# ----------------------------------------------------------

# Output: Data Mart
dm = os.path.join(downloads, "datamart.db")
conn_dm = sqlite3.connect(dm)

# Load full table
df = pd.read_sql("SELECT * FROM [Dim-BMI]", conn_dw)

# Vertical slicing → keep only selected columns
vertical = df[["Height", "Weight", "Indicator"]]

# Store in datamart
vertical.to_sql("Dim-BMI-Vertical", conn_dm, if_exists="replace", index=False)

# Print details
print("Full dataset:", df.shape)
print("Vertical sliced dataset:", vertical.shape)
