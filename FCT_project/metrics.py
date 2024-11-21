import pandas as pd
from glob import glob

def get_day_metrics(file_path):
    """Get key metrics for one day's data."""
    df = pd.read_csv(file_path)
    times = df['Travel Minutes']
    mean = times.mean()
    
    return {
        'Date': df['Date and Time'].iloc[0].split()[0],
        'Mean (min)': round(mean, 1),
        'Min (min)': times.min(),
        'Max (min)': times.max(),
        'Low Threshold': round(times.quantile(0.6), 1),
        'High Threshold': round(times.quantile(0.9), 1),
        'Total Lost Minutes': round(times[times > mean].sum() - (mean * (times > mean).sum()), 1)
    }

# note: total lost minutes calculates cumulative time lost 
# compared to if every journey took the mean time
# i think this is a great metric to model the effectiveness of my future model


def main():
    # Get metrics for all files
    files = glob('./FCT_project/data/timeseries/25Oct-to-Nov/*.csv')
    all_metrics = [get_day_metrics(f) for f in files]
    
    # Create and save dataframe
    df = pd.DataFrame(all_metrics)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    df.to_csv('./FCT_project/data/25Oct-to-Nov-metrics.csv', index=False)
    print("Metrics saved!")

if __name__ == "__main__":
    main()