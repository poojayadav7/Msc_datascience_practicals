import pandas as pd, yfinance as yf, sqlite3, os

d = os.path.join(os.path.expanduser("~"), "Downloads")
df = pd.read_csv(os.path.join(d, "VKHCG_Shares.csv"))
c = sqlite3.connect(os.path.join(d, "Shares.db"))

for s,u,t in zip(df["Shares"], df["Units"], df["sTable"]):
    try:
        x = yf.download(s, progress=False, threads=False, auto_adjust=True)
        if not x.empty:
            x["UnitsOwn"], x["ShareCode"] = u, s
            x.to_csv(os.path.join(d,f"{t}.csv"), index=False)
            x.to_sql(t, c, if_exists="replace", index=False)
            print(f"✔ {s}")
        else: print(f"❌ {s}")
    except: print(f"⚠ {s}")

c.close()
print("✔ Done")
