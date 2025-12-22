import pandas as pd, sqlite3, uuid, os

out = r"C:\Users\Administrator\Downloads"
db = os.path.join(out, "LocationData.db")

# GitHub raw input location (embedded as requested)
InputFileURL = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/01-Vermeulen/02-Assess/01-EDS/02-Python/Assess-DAG-Schedule.gml"

rows = []
for lon in range(-180, 180, 10):
    for lat in range(-90, 90, 10):
        rows.append({
            "ID": str(uuid.uuid4()),
            "LocationName": f"L{lon*1000:+07d}-{lat*1000:+07d}",
            "Longitude": lon,
            "Latitude": lat
        })

df = pd.DataFrame(rows)
conn = sqlite3.connect(db)
df.to_sql("Process_Location", conn, if_exists="replace")
df.to_sql("Hub_Location", conn, if_exists="replace")
print("DONE — Location database created in Downloads")
