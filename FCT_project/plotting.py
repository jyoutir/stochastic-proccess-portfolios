"""
Block for generating pltos from ./FCT_project/data/timeseries/25Oct-to-Nov.
Plots coloured chart of period of low medium high.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import os

def plot_and_save(csv_file, output_dir):
    data = pd.read_csv(csv_file)
    data['Date and Time'] = pd.to_datetime(data['Date and Time'])
    data['Travel Time (mins)'] = data['Travel Time'].str.split().apply(lambda x: int(x[0])*60 + int(x[-2]) if 'hour' in x else int(x[0]))

    filename = os.path.basename(csv_file)
    from_city, to_city = filename.replace('.csv', '').split('_')[0].split('-')
    date_str = filename.split('_')[1].replace('.csv', '')  # Extract date from filename
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if 'State' in data.columns:
        colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        for i in range(len(data)-1):
            ax.plot(data['Date and Time'].iloc[i:i+2], 
                   data['Travel Time (mins)'].iloc[i:i+2], 
                   color=colors[data['State'].iloc[i]], 
                   marker='o', linestyle='-')
        legend_elements = [Line2D([0], [0], color=c, label=s) for s, c in colors.items()]
        ax.legend(handles=legend_elements)
    else:
        ax.plot(data['Date and Time'], data['Travel Time (mins)'], marker='o', linestyle='-')
    
    ax.set(title=f'Travel Time from {from_city} to {to_city} ({date_str})',
           xlabel='Time', ylabel='Travel Time (minutes)')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.gcf().autofmt_xdate()
    ax.grid(True)

    min_time, max_time = data['Travel Time (mins)'].agg(['min', 'max'])
    y_range = max_time - min_time
    ax.set_ylim(max(0, min_time - 0.1 * y_range), max_time + 0.1 * y_range)

    plt.savefig(os.path.join(output_dir, filename.replace('.csv', '.png')), bbox_inches='tight')
    plt.close()

timeseries_dir = 'FCT_project/data/timeseries/25Oct-to-Nov'
figures_dir = 'FCT_project/data/figures/25Oct-to-Nov'
os.makedirs(figures_dir, exist_ok=True)

for csv_file in [f for f in os.listdir(timeseries_dir) if f.endswith('.csv')]:
    plot_and_save(os.path.join(timeseries_dir, csv_file), figures_dir)