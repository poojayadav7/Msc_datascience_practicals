import os
import pandas as pd
import sqlite3 as sq

downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# ----------- EMBEDDED GITHUB RAW INPUT (WORKING) -----------
InputFileURL = "https://raw.githubusercontent.com/chriswmann/datasets/master/500_Person_Gender_Height_Weight_Index.csv"

# Database locations in Downloads
dw_db = os.path.join(downloads, "datawarehouse.db")
dm_db = os.path.join(downloads, "datamart.db")

# Connect
dw = sq.connect(dw_db)
dm = sq.connect(dm_db)

# Load GitHub CSV into Data Warehouse
df_raw = pd.read_csv(InputFileURL)

# Prepare columns exactly as required for Dim-BMI
df_raw["PersonID"] = df_raw.index + 1
df_raw["Height"] = df_raw["Height"] / 100  # convert cm → meters
df_raw["bmi"] = df_raw["Weight"] / (df_raw["Height"] ** 2)
df_raw["Indicator"] = df_raw["Index"]

df_raw = df_raw[["PersonID", "Height", "Weight", "bmi", "Indicator"]]

df_raw.to_sql("Dim-BMI", dw, if_exists="replace", index=False)
# ----------------------------------------------------------

# Full table (for info only)
df = pd.read_sql("SELECT * FROM [Dim-BMI];", dw)

# Secure filtered table
secure_df = pd.read_sql("""
    SELECT Height, Weight, Indicator,
           CASE Indicator
                WHEN 1 THEN 'Pip'
                WHEN 2 THEN 'Norman'
                WHEN 3 THEN 'Grant'
                ELSE 'Sam'
           END AS Name
    FROM [Dim-BMI]
    WHERE Indicator > 2
    ORDER BY Height, Weight;
""", dw)

# Save secure table
secure_df.to_sql("Dim-BMI-Secure", dm, if_exists="replace", index=False)

# Load only Sam's rows (restricted view)
sam_df = pd.read_sql("SELECT * FROM [Dim-BMI-Secure] WHERE Name='Sam';", dm)

print(sam_df)
