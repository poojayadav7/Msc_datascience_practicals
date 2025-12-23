import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---- Paths ----
downloads = os.path.join(os.path.expanduser("~"), "Downloads")
# GitHub raw CSV URL from the original report code
input_file = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/01-Vermeulen/02-Assess/01-EDS/02-Python/Assess-Network-Routing-Customer.csv"
output_file = os.path.join(downloads, "Customer_Network_Map.png")

# ---- Load CSV (fix encoding) ----
try:
    df = pd.read_csv(input_file, encoding="latin-1").head(100)
except:
    df = pd.read_csv(input_file, encoding="ISO-8859-1", errors="replace").head(100)

# ---- Prepare layers like NetworkX layout ----
countries = df['Customer_Country_Name'].unique()
country_x, place_x, coord_x = 0.1, 0.5, 0.9
country_y = np.linspace(0.9, 0.1, len(countries))
pos = {}

plt.figure(figsize=(20, 10))

# ---- Country nodes ----
for c, y in zip(countries, country_y):
    pos[c] = (country_x, y)
    plt.scatter(country_x, y, s=50, color='blue')
    plt.text(country_x, y, c, fontsize=10, color='blue')

# ---- Place + Coordinate nodes ----
for i, row in df.iterrows():
    c = row['Customer_Country_Name']
    place = f"{row['Customer_Place_Name']} ({c})"
    coord = f"({row['Customer_Latitude']:.4f}, {row['Customer_Longitude']:.4f})"

    offset = np.random.uniform(-0.02, 0.02)
    py = pos[c][1] + offset

    # place node
    plt.scatter(place_x, py, s=20, color='black')
    plt.text(place_x, py, place, fontsize=8)

    # coord node
    plt.scatter(coord_x, py, s=20, color='red')
    plt.text(coord_x, py, coord, fontsize=8, color='red')

    # edges (same logic as original)
    plt.plot([country_x, place_x], [pos[c][1], py], linestyle='--', color='gray')
    plt.plot([place_x, coord_x], [py, py], linestyle='--', color='gray')

plt.axis('off')
plt.title("Customer Network Map (Simplified Layout)")
plt.savefig(output_file, dpi=300)
plt.show()

print("Saved:", output_file)
