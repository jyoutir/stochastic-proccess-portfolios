import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse  # Import Ellipse directly
from scipy.stats import norm

# Load and prepare data
data = pd.read_csv("FCT_project/data/timeseries/typical_day.csv")
data['TimeNumeric'] = data['Time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60)

# Create 2D feature matrix using both time and journey duration
X = np.column_stack((data['TimeNumeric'].values, data['Mean_Minutes'].values))

# Fit GMM with more components to capture time-varying states
n_components = 5  # Increase components to capture different times of day
gmm = GaussianMixture(n_components=n_components, 
                      covariance_type='full', 
                      random_state=42)
gmm.fit(X)

# Add component predictions to the DataFrame
data['Component'] = gmm.predict(X)

# Create figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 18))

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
                            label=f'State {i+1}', markersize=10)
                  for i in range(n_components)]
ax1.legend(handles=legend_elements)

# Plot 2: 2D visualization of states
scatter2 = ax2.scatter(data['TimeNumeric'], data['Mean_Minutes'], 
                      c=data['Component'], cmap='viridis', alpha=0.3)

# Plot the GMM components as ellipses
for i in range(n_components):
    mean = gmm.means_[i]
    covar = gmm.covariances_[i]
    
    # Calculate eigenvalues and eigenvectors
    eigenvals, eigenvecs = np.linalg.eigh(covar)
    
    # Calculate angle
    angle = np.degrees(np.arctan2(eigenvecs[1, 0], eigenvecs[0, 0]))
    
    # Calculate width and height of ellipse using eigenvalues
    width, height = 2 * np.sqrt(2) * np.sqrt(eigenvals)
    
    # Create and add the ellipse
    ellipse = Ellipse(xy=mean, width=width, height=height, angle=angle,
                      facecolor=scatter.cmap(scatter.norm(i)), alpha=0.3)
    ax2.add_patch(ellipse)

ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('Mean Minutes')
ax2.set_title('GMM States with Covariance Ellipses')
ax2.grid(True, alpha=0.3)

# Plot 3: State probabilities throughout the day
times = np.linspace(0, 24, 100)
journey_times = np.mean(data['Mean_Minutes']) * np.ones_like(times)
X_test = np.column_stack((times, journey_times))
probabilities = gmm.predict_proba(X_test)

for i in range(n_components):
    ax3.plot(times, probabilities[:, i], 
             label=f'State {i+1}', alpha=0.7)
ax3.set_xlabel('Time (hours)')
ax3.set_ylabel('State Probability')
ax3.set_title('State Probabilities Throughout the Day')
ax3.grid(True, alpha=0.3)
ax3.legend()

plt.tight_layout()
plt.show()

# Print summary statistics for each state
print("\nTraffic State Analysis:")
print("------------------------")
for i in range(n_components):
    mean_time = gmm.means_[i][0]
    mean_duration = gmm.means_[i][1]
    weight = gmm.weights_[i]
    
    # Convert time to hours:minutes format
    hours = int(mean_time)
    minutes = int((mean_time - hours) * 60)
    time_str = f"{hours:02d}:{minutes:02d}"
    
    print(f"\nState {i+1}:")
    print(f"Peak Time: {time_str}")
    print(f"Mean Journey Duration: {mean_duration:.2f} minutes")
    print(f"Weight: {weight:.3f} ({weight*100:.1f}% of data)")
    
    # Calculate and print the time range where this state is dominant
    state_probs = probabilities[:, i]
    dominant_times = times[state_probs > 0.5]
    if len(dominant_times) > 0:
        start_time = int(dominant_times[0])
        end_time = int(dominant_times[-1])
        print(f"Dominant Period: {start_time:02d}:00 - {end_time:02d}:00")

# Save the enhanced state parameters
state_params = pd.DataFrame({
    'State': range(1, n_components + 1),
    'Mean_Time': gmm.means_[:, 0],
    'Mean_Duration': gmm.means_[:, 1],
    'Time_Variance': gmm.covariances_[:, 0, 0],
    'Duration_Variance': gmm.covariances_[:, 1, 1],
    'Weight': gmm.weights_
})

print("\nState Parameters:")
print(state_params)
state_params.to_csv("FCT_project/data/traffic_states.csv", index=False)