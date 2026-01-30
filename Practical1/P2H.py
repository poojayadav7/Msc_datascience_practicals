import imageio.v2 as imageio
import pandas as pd
import numpy as np
import os

# Downloads folder
downloads = r"C:\Users\Administrator\Downloads"

# Input & Output
input_url = "https://github.com/Apress/practical-data-science/blob/master/VKHCG/05-DS/9999-Data/Angus.jpg?raw=true"
output_file = os.path.join(downloads, "HORUS_Picture.csv")

# Read image directly from GitHub URL
img = imageio.imread(input_url)

# Convert to HORUS format
h, w, c = img.shape
pixels = img.reshape(-1, c)
df = pd.DataFrame(pixels, columns=["Red", "Green", "Blue", "Alpha"][:c])

# Save HORUS CSV
df.to_csv(output_file, index=False)

print("Picture successfully converted to HORUS format in Downloads")
