import os, uuid, pandas as pd, sqlite3
from pytz import timezone, all_timezones
from datetime import datetime, timedelta
from random import randint

# Downloads folder
downloads = r"C:\Users\Administrator\Downloads"

# GitHub raw CSV URL
InputFileURL = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/04-Clark/02-Assess/01-EDS/02-Python/Assess_People.csv"
df = pd.read_csv(InputFileURL)

# Clean column names
df.columns = df.columns.str.replace(" ", "").str.strip()  # removes spaces
# Now columns are: FirstName, SecondName, LastName, Gender

# Birth details
start = datetime(1900,1,1).replace(tzinfo=timezone("UTC"))
hrs = 100 * 365 * 24
df["BirthDateUTC"] = [start + timedelta(hours=randint(0, hrs)) for _ in range(len(df))]
df["TimeZone"] = [all_timezones[randint(0, len(all_timezones)-1)] for _ in range(len(df))]

df["BirthDateISO"] = [utc.astimezone(timezone(tz)) for utc, tz in zip(df["BirthDateUTC"], df["TimeZone"])]
df["BirthDateISO"] = [dt.replace(tzinfo=None) for dt in df["BirthDateISO"]]

df["BirthDate"] = pd.to_datetime(df["BirthDateISO"]).dt.strftime("%Y-%m-%d %H:%M:%S")
df["BirthDateKey"] = df["BirthDateUTC"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["PersonID"] = [str(uuid.uuid4()) for _ in range(len(df))]

# Output DBs
db1 = os.path.join(downloads, "Process_People.db")
db2 = os.path.join(downloads, "DataVault_People.db")
conn1, conn2 = sqlite3.connect(db1), sqlite3.connect(db2)

# Process table
df.set_index("PersonID").to_sql("Process_Person", conn1, if_exists="replace")

# Hub + Satellite tables
df[["PersonID","FirstName","SecondName","LastName","BirthDateKey"]].drop_duplicates()\
    .set_index("PersonID").to_sql("Hub_Person", conn2, if_exists="replace")
df[["PersonID","Gender"]].set_index("PersonID")\
    .to_sql("Satellite_PPerson_Gender", conn2, if_exists="replace")
df[["PersonID","TimeZone","BirthDate"]].set_index("PersonID")\
    .to_sql("Satellite_PPerson_Names", conn2, if_exists="replace")

# CSV export
df.to_csv(os.path.join(downloads, "Process_People.csv"), index=False)

print("✔ Completed! Files saved in Downloads folder.")
