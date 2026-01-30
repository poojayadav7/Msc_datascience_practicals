import pandas as pd
import sqlite3
import os
import urllib.request

# Downloads folder
downloads = r"C:\Users\Administrator\Downloads"

# Database URL & local path
db_url = "https://github.com/Apress/practical-data-science/raw/refs/heads/master/VKHCG/05-DS/9999-Data/utility.db"
db_file = os.path.join(downloads, "utility.db")

table = "Country_Code"
output_file = os.path.join(downloads, "HORUS_Country.csv")

# Download DB if not already present
if not os.path.exists(db_file):
    urllib.request.urlretrieve(db_url, db_file)

# Read table from database
with sqlite3.connect(db_file) as conn:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)

# HORUS transformation
df = (
    df.drop(columns=["ISO-2-CODE", "ISO-3-Code"])
      .rename(columns={"Country": "CountryName", "ISO-M49": "CountryNumber"})
      .sort_values("CountryName", ascending=False)
)

# Save HORUS CSV
df.to_csv(output_file, index=False)

print("Database successfully converted to HORUS format in Downloads")
