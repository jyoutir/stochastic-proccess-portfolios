import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def original_arrival_rate(t, base_rate=40):
    peaks = [
        {"amplitude": 90, "time": 420, "width": 90},  # 7 AM
        {"amplitude": 30, "time": 660, "width": 120},  # 11 AM
        {"amplitude": 80, "time": 900, "width": 120},  # 3 PM
    ]
    
    rate = base_rate
    for peak in peaks:
        A = peak["amplitude"]
        t_peak = peak["time"]
        sigma = peak["width"]
        rate += A * np.exp(-((t - t_peak)**2) / (2 * sigma**2))
    
    return max(rate, base_rate)

def staggered_arrival_rate(t, base_rate=40):
    peaks = [
        {"amplitude": 45, "time": 300, "width": 90},   # 5 AM
        {"amplitude": 45, "time": 480, "width": 90},   # 8 AM
        {"amplitude": 30, "time": 660, "width": 120},  # 11 AM
        {"amplitude": 35, "time": 780, "width": 120},  # 1 PM
        {"amplitude": 45, "time": 960, "width": 120},  # 4 PM
    ]
    
    rate = base_rate
    for peak in peaks:
        A = peak["amplitude"]
        t_peak = peak["time"]
        sigma = peak["width"]
        rate += A * np.exp(-((t - t_peak)**2) / (2 * sigma**2))
    
    return max(rate, base_rate)

def load_real_data():
    typical_day = pd.read_csv('FCT_project/data/timeseries/typical_day.csv')
    times = []
    for time_str in typical_day['Time']:
        hours, minutes = map(int, time_str.split(':'))
        minutes_since_midnight = hours * 60 + minutes
        times.append(minutes_since_midnight)
    
    return times, typical_day['Mean_Minutes'].values

# Create time points
time_points = np.arange(0, 1441)

# Calculate arrival rates
original_rates = [original_arrival_rate(t) for t in time_points]
staggered_rates = [staggered_arrival_rate(t) for t in time_points]

# Load real data
times_real, real_data = load_real_data()

# Create figure with two y-axes
fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

# Plot arrival rate models on primary y-axis
ax1.plot(time_points, original_rates, 
         color='green', linewidth=2,  
         label='Typical Day Arrival Rate Estimate')
ax1.plot(time_points, staggered_rates, 
         color='red', linewidth=2, 
         label='Staggered Start Times Policy Arrival Rate')

# Plot real traffic data on secondary y-axis
ax2.plot(times_real, real_data, 
         color='#2E86C1', linewidth=2.5, 
         label='TDM\'s Traffic Data')

# Create time ticks in HH:MM format - show every 3 hours
xticks = np.arange(0, 1441, 180)  # Every 3 hours (180 minutes)
times = [f"{h:02d}:00" for h in range(0, 25, 3)]  # Create labels for every 3 hours
plt.xticks(xticks, times, 
           rotation=45,
           ha='right')

# Set labels and title
ax1.set_xlabel('Time of Day', fontsize=10, color='black')  # Set to black
ax1.set_ylabel('Arrival Rate (vehicles per minute)', fontsize=10, color='black')  # Set to black
ax2.set_ylabel('Travel Time (minutes)', color='black', fontsize=10)

# Make axis colors black
ax1.tick_params(axis='both', colors='black')  # Set tick colors to black
ax2.tick_params(axis='y', colors='black')   # Keep secondary y-axis in blue
ax1.spines['left'].set_color('black')         # Set spine colors to black
ax1.spines['bottom'].set_color('black')       # Set spine colors to black

plt.title('Comparison of TDM\'s Traffic Patterns to Arrival Rate functions', fontsize=12)

# Set y-axis limits for arrival rate (primary axis)
ax1.set_ylim(bottom=0)

# Add both legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

# Grid and spine visibility
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.tight_layout()
plt.savefig('FCT_project/data/traffic_patterns.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.show()
plt.close()
