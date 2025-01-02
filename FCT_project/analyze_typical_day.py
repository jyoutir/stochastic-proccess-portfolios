import pandas as pd
import numpy as np

# Read the typical day data
df = pd.read_csv('./FCT_project/data/timeseries/typical_day.csv')

# Calculate overall average
overall_mean = df['Mean_Minutes'].mean()

# Calculate peak and off-peak averages
peak_morning = df[(df['Time'] >= '07:00') & (df['Time'] <= '09:00')]['Mean_Minutes'].mean()
peak_afternoon = df[(df['Time'] >= '15:00') & (df['Time'] <= '18:00')]['Mean_Minutes'].mean()
off_peak = df[~((df['Time'] >= '07:00') & (df['Time'] <= '09:00')) & 
              ~((df['Time'] >= '15:00') & (df['Time'] <= '18:00'))]['Mean_Minutes'].mean()

print(f"\nRoute Analysis: Enniskillen to Belfast")
print(f"----------------------------------------")
print(f"Overall average journey time: {overall_mean:.1f} minutes ({overall_mean/60:.1f} hours)")
print(f"\nPeak Times:")
print(f"Morning peak (7-9am): {peak_morning:.1f} minutes ({peak_morning/60:.1f} hours)")
print(f"Afternoon peak (3-6pm): {peak_afternoon:.1f} minutes ({peak_afternoon/60:.1f} hours)")
print(f"Off-peak average: {off_peak:.1f} minutes ({off_peak/60:.1f} hours)")

# Calculate time differences
print(f"\nImpact of Peak Times:")
print(f"Morning peak adds: {peak_morning - off_peak:.1f} minutes")
print(f"Afternoon peak adds: {peak_afternoon - off_peak:.1f} minutes") 