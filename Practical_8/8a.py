import pandas as pd
import sqlite3
import os

downloads = r"C:/Users/Administrator/Downloads"

# ----------- VERIFIED GITHUB RAW INPUT (WORKING) -----------
InputFileURL = "https://raw.githubusercontent.com/chriswmann/datasets/master/500_Person_Gender_Height_Weight_Index.csv"

dw = os.path.join(downloads, "datawarehouse.db")
conn_dw = sqlite3.connect(dw)

# Load GitHub CSV
df_raw = pd.read_csv(InputFileURL)

# Prepare columns EXACTLY as required (no logic change later)
df_raw["PersonID"] = df_raw.index + 1
df_raw["Height"] = df_raw["Height"] / 100   # cm → meters
df_raw["bmi"] = df_raw["Weight"] / (df_raw["Height"] ** 2)
df_raw["Indicator"] = df_raw["Index"]

df_raw = df_raw[["PersonID", "Height", "Weight", "bmi", "Indicator"]]

df_raw.to_sql("Dim-BMI", conn_dw, if_exists="replace", index=False)
# ----------------------------------------------------------

dm = os.path.join(downloads, "datamart.db")
conn_dm = sqlite3.connect(dm)

df = pd.read_sql("SELECT * FROM [Dim-BMI]", conn_dw)

filtered = df[(df["Height"] > 1.5) & (df["Indicator"] == 1)]

filtered.to_sql("Dim-BMI", conn_dm, if_exists="replace", index=False)

print("Full rows:", df.shape[0])
print("Filtered rows:", filtered.shape[0])
