import os
import matplotlib.pyplot as plt
from sklearn import manifold
import pandas as pd

# Use a real raw MNIST test CSV from GitHub
url = "https://raw.githubusercontent.com/dbdmg/data-science-lab/master/datasets/mnist_test.csv"

# Load CSV: first column = label, others = pixels
df = pd.read_csv(url, header=None)
y = df.iloc[:, 0].values
X = df.iloc[:, 1:].values

# t-SNE reduction
X_2d = manifold.TSNE(n_components=2, random_state=0).fit_transform(X)

# Plot
plt.figure(figsize=(8, 8))
for i in range(len(X_2d)):
    plt.scatter(X_2d[i, 0], X_2d[i, 1], c=y[i], cmap='tab10', s=5)
plt.title("t-SNE Visualization of MNIST Test Digits")

# Save
out = os.path.join(os.path.expanduser("~"), "Downloads", "Container_Digit_Visualization.png")
plt.savefig(out)
plt.show()

print("Saved:", out)
