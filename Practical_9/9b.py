import os
import pandas as pd
import folium
from folium.plugins import FastMarkerCluster, HeatMap

# Paths
downloads = os.path.join(os.path.expanduser("~"), "Downloads")
# GitHub raw CSV URL from original report code
input_file = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/02-Krennwallner/01-Retrieve/01-EDS/02-Python/Retrieve_DE_Billboard_Locations.csv"

# Load data
df = pd.read_csv(input_file, encoding="latin-1").fillna(0)

# Keep valid coords
df = df[(df["Latitude"] != 0) & (df["Longitude"] != 0)]
locations = df[["Latitude", "Longitude"]].values.tolist()

# --- 1) Cluster Map ---
cluster_map = folium.Map(location=[48.1459806, 11.4985484], zoom_start=5)
FastMarkerCluster(locations).add_to(cluster_map)
cluster_map.save(os.path.join(downloads, "Billboard_Cluster.html"))

# --- 2) Pins Map ---
pins_map = folium.Map(location=[48.1459806, 11.4985484], zoom_start=5)
for _, row in df.head(100).iterrows():
    folium.Marker([row["Latitude"], row["Longitude"]], popup=row["Place_Name"]).add_to(pins_map)
pins_map.save(os.path.join(downloads, "Billboard_Pins.html"))

# --- 3) Heat Map ---
heat_map = folium.Map(location=[48.1459806, 11.4985484], zoom_start=5)
HeatMap(locations[:100]).add_to(heat_map)
heat_map.save(os.path.join(downloads, "Billboard_Heatmap.html"))

print("All 3 maps saved in Downloads folder!")
