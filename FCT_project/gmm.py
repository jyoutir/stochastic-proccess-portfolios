# FCT_project/gmm.py

import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load and prepare data
data = pd.read_csv("FCT_project/data/timeseries/typical_day.csv")
data['TimeNumeric'] = data['Time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60)

# Prepare the feature matrix
X = data['Mean_Minutes'].values.reshape(-1, 1)

# Fit GMM
gmm = GaussianMixture(n_components=3, covariance_type='full', random_state=42)
gmm.fit(X)

# Add component predictions to the DataFrame
data['Component'] = gmm.predict(X)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

# Plot 1: Time series with components
scatter = ax1.scatter(data['TimeNumeric'], data['Mean_Minutes'], 
                     c=data['Component'], cmap='viridis', alpha=0.6)
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Mean Minutes')
ax1.set_title('Traffic Patterns Throughout the Day')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(0, 25, 2))

# Add legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                            markerfacecolor=scatter.cmap(scatter.norm(i)), 
                            label=f'Component {i+1}', markersize=10)
                  for i in range(3)]
ax1.legend(handles=legend_elements)

# Plot 2: Gaussian components
x = np.linspace(min(data['Mean_Minutes']), max(data['Mean_Minutes']), 200)
total_pdf = np.zeros_like(x)
for i in range(3):
    mean = gmm.means_[i][0]
    var = gmm.covariances_[i][0][0]
    weight = gmm.weights_[i]
    std_dev = np.sqrt(var)
    
    y = weight * norm.pdf(x, mean, std_dev)
    total_pdf += y  # Sum up for the overall distribution
    ax2.plot(x, y, label=f'Component {i+1}\n(μ={mean:.2f}, σ²={var:.2f}, w={weight:.2f})')

ax2.set_xlabel('Mean Minutes')
ax2.set_ylabel('Density')
ax2.set_title('Gaussian Components of the Mixture Model')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.show()

# Print summary statistics
print("\nGaussian Mixture Model Components Summary:")
print("------------------------------------------")
for i in range(3):
    mean = gmm.means_[i][0]
    var = gmm.covariances_[i][0][0]
    weight = gmm.weights_[i]
    std_dev = np.sqrt(var)
    
    print(f"\nComponent {i+1}:")
    print(f"Mean Journey Time (μ): {mean:.2f} minutes")
    print(f"Variance (σ²): {var:.4f} (Standard Deviation σ: {std_dev:.2f} minutes)")
    print(f"Weight (w): {weight:.4f} ({weight*100:.2f}% of data)")

# Output component parameters as a DataFrame
components_df = pd.DataFrame({
    'Component': [1, 2, 3],
    'Mean_Minutes': gmm.means_.flatten(),
    'Variance': gmm.covariances_.flatten(),
    'Weight': gmm.weights_.flatten()
})

print("\nComponent Parameters DataFrame:")
print(components_df)

# Save the parameters for use in model.ipynb
components_df.to_csv("FCT_project/data/gmm_components.csv", index=False)
