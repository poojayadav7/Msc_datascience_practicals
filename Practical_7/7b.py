import pandas as pd, sqlite3, os, uuid
from datetime import datetime
from pytz import timezone

# ---- Input raw file (embedded only, no logic change) ----
InputFileURL = "https://raw.githubusercontent.com/Apress/practical-data-science/master/VKHCG/01-Vermeulen/00-RawData/VehicleData.csv"

d = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(d, exist_ok=True)

# ---- Time dimension ----
utc = datetime(1960,12,20,10,15,0, tzinfo=timezone('UTC'))
local = utc.astimezone(timezone('Atlantic/Reykjavik'))
time_id = str(uuid.uuid4())
time_df = pd.DataFrame([{
    'TimeID': time_id,
    'UTCDate': utc,
    'LocalTime': local,
    'TimeZone':'Atlantic/Reykjavik'
}])
time_df.to_csv(os.path.join(d,'Dim-Time.csv'), index=False)

# ---- Person dimension ----
person_id = str(uuid.uuid4())
person_df = pd.DataFrame([{
    'PersonID': person_id,
    'FirstName':'Guðmundur',
    'LastName':'Gunnarsson',
    'Zone':'UTC',
    'DateTimeValue':utc
}])
person_df.to_csv(os.path.join(d,'Dim-Person.csv'), index=False)

# ---- Fact table ----
fact_df = pd.DataFrame([{
    'IDNumber': str(uuid.uuid4()),
    'PersonID': person_id,
    'TimeID': time_id
}])
fact_df.to_csv(os.path.join(d,'Fact-Person-Time.csv'), index=False)

# ---- Save to SQLite ----
for db_name in ['datavault.db','datawarehouse.db']:
    conn = sqlite3.connect(os.path.join(d, db_name))
    time_df.set_index('TimeID').to_sql('Dim-Time', conn, if_exists='replace')
    person_df.set_index('PersonID').to_sql('Dim-Person', conn, if_exists='replace')
    fact_df.set_index('IDNumber').to_sql('Fact-Person-Time', conn, if_exists='replace')
    conn.close()

print("✔ Done. CSVs and SQLite DBs are in Downloads folder.")
