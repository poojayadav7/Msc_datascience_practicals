import pandas as pd

# File paths
base = r'C:/Users/Administrator/Downloads'
input_url = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/01-Vermeulen/00-RawData/IP_DATA_CORE.csv"
output_file = f'{base}/Retrieve_Router_Location.csv'

# Load CSV directly from GitHub
df = pd.read_csv(input_url, encoding='latin-1', low_memory=False)

# Rename column
df.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Select needed columns and calculate mean latitude
mean_data = (
    df[['Country', 'Place_Name', 'Latitude']]
    .groupby(['Country', 'Place_Name'])['Latitude']
    .mean()
)

# Save result
mean_data.to_csv(output_file)

print("Router location data successfully saved in Downloads")
