import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

# Parameters
average_time_min = 2
std_dev_min = 1
mean_seconds_per_word = 8
std_seconds_per_word = 1
daily_participation_rate = 0.85
num_users = 100000
num_simulations = 1000

# Calculate gamma parameters BEFORE the simulation loop
theta = (std_dev_min ** 2) / average_time_min
k = (average_time_min / theta)

# Store histogram data for each simulation
hist_data = []
for _ in range(num_simulations):
    uses_app = np.random.random(num_users) < daily_participation_rate
    time_spent_minutes = np.zeros(num_users)
    time_spent_minutes[uses_app] = gamma.rvs(a=k, scale=theta, size=np.sum(uses_app))
    time_spent_minutes = np.clip(time_spent_minutes, 0, 60)
    
    seconds_per_word = np.random.normal(mean_seconds_per_word, std_seconds_per_word, num_users)
    seconds_per_word = np.maximum(seconds_per_word, 1)
    
    words_per_user = (time_spent_minutes * 60) / seconds_per_word
    hist_counts, _ = np.histogram(words_per_user, bins=50)
    hist_data.append(hist_counts)

# Calculate mean and standard deviation for each bin
hist_mean = np.mean(hist_data, axis=0)
hist_std = np.std(hist_data, axis=0)

# Generate one final set of data for the main histogram
uses_app = np.random.random(num_users) < daily_participation_rate
time_spent_minutes = np.zeros(num_users)
time_spent_minutes[uses_app] = gamma.rvs(a=k, scale=theta, size=np.sum(uses_app))
time_spent_minutes = np.clip(time_spent_minutes, 0, 60)

seconds_per_word = np.random.normal(mean_seconds_per_word, std_seconds_per_word, num_users)
seconds_per_word = np.maximum(seconds_per_word, 1)

words_per_user = (time_spent_minutes * 60) / seconds_per_word

# Calculate percentiles
percentile_25 = np.percentile(words_per_user, 20)
percentile_75 = np.percentile(words_per_user, 80)

# Final plot with error bars
plt.figure(figsize=(10, 6))
counts, bins, _ = plt.hist(words_per_user, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
bin_centers = (bins[:-1] + bins[1:]) / 2

# Add error bars
plt.errorbar(bin_centers, counts, yerr=hist_std, fmt='none', color='blue', alpha=0.5)

plt.axvspan(percentile_25, percentile_75, color='blue', alpha=0.2, label='IQR (20-80th percentile)')
plt.axvline(x=percentile_25, color='b', linestyle='--')
plt.axvline(x=percentile_75, color='b', linestyle='--')
plt.title('Distribution of Words Covered per User')
plt.xlabel('Words Covered')
plt.ylabel('Number of Users')
plt.grid(True)
plt.legend()
plt.savefig('portfolio_X/figure1.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"20th percentile: {percentile_25:.1f} words")
print(f"80th percentile: {percentile_75:.1f} words")
