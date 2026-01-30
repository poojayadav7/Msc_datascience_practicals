import pandas as pd
import os

# Downloads folder (Administrator)
downloads = r"C:\Users\Administrator\Downloads"

# Input & Output files
input_url = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/01-Vermeulen/00-RawData/Country_Code.csv"
output_file = os.path.join(downloads, "HORUS_Country.csv")

# Read CSV directly from GitHub raw URL
df = pd.read_csv(input_url, encoding="latin-1")

# Convert to HORUS format
df = (
    df.drop(columns=["ISO-2-CODE", "ISO-3-Code"])
      .rename(columns={"Country": "CountryName", "ISO-M49": "CountryNumber"})
      .sort_values("CountryName", ascending=False)
)

# Save HORUS CSV
df.to_csv(output_file, index=False)

print("CSV successfully converted to HORUS format in Downloads")
