import pandas as pd
import os

# Downloads folder
downloads = r"C:\Users\Administrator\Downloads"

# Input & Output files
input_url = "https://github.com/Apress/practical-data-science/raw/refs/heads/master/VKHCG/05-DS/9999-Data/Country_Code.json"
output_file = os.path.join(downloads, "HORUS_Country.csv")

# Read JSON directly from GitHub raw URL
df = pd.read_json(input_url, orient="index")

# HORUS transformation
df = (
    df.drop(columns=["ISO-2-CODE", "ISO-3-Code"])
      .rename(columns={"Country": "CountryName", "ISO-M49": "CountryNumber"})
      .sort_values("CountryName", ascending=False)
)

# Save HORUS CSV
df.to_csv(output_file, index=False)

print("JSON successfully converted to HORUS format in Downloads")
