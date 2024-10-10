import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
csv_file_path = './data/Enn-Bel_25thDec.csv'
data = pd.read_csv(csv_file_path)

data['Date and Time'] = pd.to_datetime(data['Date and Time'])

# convert travel time to mins
def convert_to_minutes(travel_time_str):
    parts = travel_time_str.split()
    hours = int(parts[0]) if 'hour' in parts else 0
    minutes = int(parts[2]) if 'mins' in parts else 0
    return hours * 60 + minutes

data['Travel Time (mins)'] = data['Travel Time'].apply(convert_to_minutes)


plt.figure(figsize=(12, 6))
plt.plot(data['Date and Time'], data['Travel Time (mins)'], marker='o', linestyle='-')
plt.title('Travel Time from Enniskillen to Belfast on 25th Dec 2025')
plt.xlabel('Date and Time')
plt.ylabel('Travel Time (minutes)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()