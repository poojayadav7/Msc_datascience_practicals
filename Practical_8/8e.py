import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# GitHub RAW Excel input
InputFileURL = "https://raw.githubusercontent.com/fenago/datasets/main/Online%20Retail.xlsx"

# Specify engine for online Excel
df = pd.read_excel(InputFileURL, engine="openpyxl")

output = os.path.join(downloads, "Output")
os.makedirs(output, exist_ok=True)

# Clean data
df = df.dropna(subset=['InvoiceNo'])
df['InvoiceNo'] = df['InvoiceNo'].astype(str)
df = df[~df['InvoiceNo'].str.contains('C')]
df['Description'] = df['Description'].str.strip()

# Encode as boolean
def rules(country, sup, lift, conf, filename):
    basket = (df[df['Country']==country]
              .groupby(['InvoiceNo','Description'])['Quantity']
              .sum().unstack().fillna(0).astype(bool))
    
    basket.drop('POSTAGE', axis=1, errors='ignore', inplace=True)

    items = apriori(basket, min_support=sup, use_colnames=True)
    res = association_rules(items, metric="lift", min_threshold=1)
    strong = res[(res.lift >= lift) & (res.confidence >= conf)]
    strong.to_csv(os.path.join(output, filename), index=False)
    return strong

print(rules("France", 0.07, 6, 0.8, "France_Rules.csv"))
print(rules("Germany", 0.05, 4, 0.5, "Germany_Rules.csv"))
