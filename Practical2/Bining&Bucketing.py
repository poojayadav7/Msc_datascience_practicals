import numpy as np
import matplotlib.pyplot as plt
from math import exp, sqrt, pi

# Fix random values so output is always the same
np.random.seed(0)

# Mean and standard deviation
mu = 90
sigma = 25

# Generate 5000 random values
x = mu + sigma * np.random.randn(5000)

# Number of bars in histogram
num_bins = 25

# Create figure and axis
fig, ax = plt.subplots()

# Draw histogram
ax.hist(x, num_bins, density=True, alpha=0.6)

# Function for normal distribution
def normal_pdf(x, mu, sigma):
    return (1 / (sigma * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sigma) ** 2)

# Create curve values
bins = np.linspace(min(x), max(x), num_bins)
y = [normal_pdf(b, mu, sigma) for b in bins]

# Plot normal curve
ax.plot(bins, y, '--')

# Labels
ax.set_xlabel('Example Data')
ax.set_ylabel('Probability Density')

# Title
ax.set_title(f'Histogram of {len(x)} values with {num_bins} bins\nμ={mu}, σ={sigma}')

# Adjust layout
fig.tight_layout()

# Save image
fig.savefig('DU-Histogram.png')

# Show plot
plt.show()

