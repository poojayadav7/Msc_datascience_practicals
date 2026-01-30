import pandas as pd

# Input CSV from GitHub
input_url = "https://media.githubusercontent.com/media/Apress/practical-data-science/refs/heads/master/VKHCG/01-Vermeulen/00-RawData/IP_DATA_CORE.csv"

# Read required columns
df = pd.read_csv(
    input_url,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding='latin-1'
)

# Rename column
df.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Keep only London rows
london = df[df['Place_Name'] == 'London']

# Select needed columns
data = london[['Country', 'Place_Name', 'Latitude']]

# Mean and standard deviation
mean_lat = data['Latitude'].mean()
std_lat = data['Latitude'].std()

# Bounds
upper = mean_lat + std_lat
lower = mean_lat - std_lat

# Outliers and non-outliers
out_high = data[data['Latitude'] > upper]
out_low = data[data['Latitude'] < lower]
not_out = data[(data['Latitude'] >= lower) & (data['Latitude'] <= upper)]

# Print results
print("All London Data:\n", data)
print("\nUpper Bound:", upper)
print("Lower Bound:", lower)
print("\nOutliers Higher:\n", out_high)
print("\nOutliers Lower:\n", out_low)
print("\nNot Outliers:\n", not_out)
