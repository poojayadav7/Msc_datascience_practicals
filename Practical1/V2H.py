import imageio.v2 as imageio
import pandas as pd
import numpy as np
import os
import urllib.request

# Downloads paths
downloads = r"C:\Users\Administrator\Downloads"
frames_dir = os.path.join(downloads, "video_frames")
output_file = os.path.join(downloads, "HORUS_Movie_Frames.csv")

video_url = "https://github.com/Apress/practical-data-science/raw/refs/heads/master/VKHCG/05-DS/9999-Data/Dog.mp4"
video_file = os.path.join(downloads, "Dog.mp4")

os.makedirs(frames_dir, exist_ok=True)

# Download video if needed
if not os.path.exists(video_file):
    urllib.request.urlretrieve(video_url, video_file)

# ---- FRAME EXTRACTION (FIXED) ----
reader = imageio.get_reader(video_file, format="ffmpeg")

frame_count = 0
for i, frame in enumerate(reader):
    frame_path = os.path.join(frames_dir, f"frame_{i}.jpg")
    imageio.imwrite(frame_path, frame)
    frame_count += 1

reader.close()

if frame_count == 0:
    raise RuntimeError("No frames extracted. Video codec not supported.")

# ---- EXISTING LOGIC (UNCHANGED) ----
all_frames = []

for file in os.listdir(frames_dir):
    if file.endswith(".jpg"):
        img = imageio.imread(os.path.join(frames_dir, file))
        pixels = img.reshape(-1, img.shape[2])
        df = pd.DataFrame(pixels, columns=["Red", "Green", "Blue"][:img.shape[2]])
        df["FrameName"] = file
        all_frames.append(df)

# Safe concatenate
horus_df = pd.concat(all_frames, ignore_index=True)

# Save HORUS CSV
horus_df.to_csv(output_file, index=False)

print("Movie frames successfully converted to HORUS format in Downloads")
