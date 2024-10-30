"""
This is code for portfolio VII. Here I simulate a 'typical day' using the 30 days of
data i have from the FCT Project on the Enniskillen -> Belfast route. 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import glob


# function to load all data. 
def load_all_data(folder_path):
    all_data = []
    for file in glob.glob(f"{folder_path}/Enn-Bel_*.csv"):
        df = pd.read_csv(file)
        df['Date and Time'] = pd.to_datetime(df['Date and Time'])
        df['Time'] = df['Date and Time'].dt.time
        all_data.append(df)
    return all_data


# creating a typical dat mnodel with CI + saving to csv. 
def create_typical_day_model(all_data, output_path='./typical_day_stats.csv'):
    # Combine all dataframes + group by time to calc stats
    combined_df = pd.concat(all_data)
    typical_day = combined_df.groupby('Time').agg({
        'Travel Minutes': ['mean', 'std', 'min', 'max']
    }).reset_index()
    
    # calc culate 95% confidence intervals
    n_samples = len(all_data)  # number of days
    typical_day['ci_lower'] = typical_day[('Travel Minutes', 'mean')] - \
                             1.96 * typical_day[('Travel Minutes', 'std')] / np.sqrt(n_samples)
    typical_day['ci_upper'] = typical_day[('Travel Minutes', 'mean')] + \
                             1.96 * typical_day[('Travel Minutes', 'std')] / np.sqrt(n_samples)
    
    export_df = pd.DataFrame({
        'Time': [t.strftime('%H:%M') for t in typical_day['Time']],
        'Mean_Minutes': typical_day[('Travel Minutes', 'mean')],
        'CI_Lower': typical_day['ci_lower'],
        'CI_Upper': typical_day['ci_upper']
    })

    # savce to csv and return the stats for plotting in next fn
    export_df.to_csv(output_path, index=False)
    return typical_day


# plotting graph thingie. 
def plot_typical_day(typical_day):
    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
    x = [t.strftime('%H:%M') for t in typical_day['Time']]
    y = typical_day[('Travel Minutes', 'mean')]
    
    # plot mean
    ax.plot(x, y, 
           color='#2E86C1', 
           linewidth=2, 
           label='Mean Travel Time')
    
    # plot CI
    ax.fill_between(x, 
                   typical_day['ci_lower'], 
                   typical_day['ci_upper'],
                   color='#2E86C1', 
                   alpha=0.2, 
                   label='95% Confidence Interval')
    
    ax.set_xlabel('Time of Day', fontsize=10)
    ax.set_ylabel('Travel Time (minutes)', fontsize=10)
    ax.set_title('Typical Daily Travel Time Pattern, sampled from 30 days of traffic data', fontsize=12)

    plt.xticks(x[::6], 
              rotation=45,
              ha='right')
    
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')
    ymin = min(typical_day['ci_lower']) - 1
    ymax = max(typical_day['ci_upper']) + 1
    ax.set_ylim(ymin, ymax)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('./portfolio_VII/figure_1.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white')
    plt.close()


def main():
    data_folder = "./FCT_project/data/timeseries/25Oct-to-Nov"
    
    all_data = load_all_data(data_folder)
    typical_day = create_typical_day_model(all_data, './portfolio_VII/typical_day_stats.csv')
    plot_typical_day(typical_day)

if __name__ == "__main__":
    main()
