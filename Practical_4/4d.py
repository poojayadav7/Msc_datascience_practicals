import os
import pandas as pd

# Base folder
base = 'C:/Users/Administrator'

# Input dataset location
file_path = base + '/Downloads/IP_DATA_ALL.csv'
print('Loading:', file_path)

# Read CSV file
df = pd.read_csv(file_path, header=0, low_memory=False, encoding="latin-1")

# Output folder
output_dir = base + '/Retrieve'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print('Rows:', df.shape[0])
print('Columns:', df.shape[1])

# Fix column names: remove spaces and replace with dots
df.columns = [col.strip().replace(" ", ".") for col in df.columns]
print('Column names fixed.')

# Add RowID index
df.index.names = ['RowID']

# Save cleaned dataset
output_file = output_dir + '/Retrieve_IP_DATA.csv'
df.to_csv(output_file, index=True, encoding="latin-1")

print('File saved as:', output_file)
print('Completed!')
