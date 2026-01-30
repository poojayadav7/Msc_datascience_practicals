import pandas as pd
import xml.etree.ElementTree as ET
import os
import urllib.request

# Downloads folder
downloads = r"C:\Users\Administrator\Downloads"

# Input & Output
input_url = "https://raw.githubusercontent.com/Apress/practical-data-science/refs/heads/master/VKHCG/05-DS/9999-Data/Country_Code.xml"
output_file = os.path.join(downloads, "HORUS_Country.csv")

# Read XML from URL
with urllib.request.urlopen(input_url) as response:
    tree = ET.parse(response)
    root = tree.getroot()

# XML to DataFrame
data = [{child.tag: child.text for child in entry} for entry in root]
df = pd.DataFrame(data)

# HORUS transformation
df = (
    df.drop(columns=["ISO-2-CODE", "ISO-3-Code"])
      .rename(columns={"Country": "CountryName", "ISO-M49": "CountryNumber"})
      .sort_values("CountryName", ascending=False)
)

# Save HORUS CSV
df.to_csv(output_file, index=False)

print("XML successfully converted to HORUS format in Downloads")
