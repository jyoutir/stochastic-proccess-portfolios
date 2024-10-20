"""
Block for generating transition matricies from ./FCT_project/data/timeseries/25Oct-to-Nov
"""

import pandas as pd

def convert_to_minutes(travel_time):
    """Convert travel time in e.g '1 hour 30 mins' format -> total minutes."""
    time_parts = travel_time.split()
    hours = int(time_parts[0])
    minutes = int(time_parts[2])
    return hours * 60 + minutes

def assign_state(minutes, low_threshold, high_threshold):
    """Assign a state based on travel time in minutes."""
    if minutes < low_threshold:
        return 'Low'
    elif low_threshold <= minutes <= high_threshold:
        return 'Medium'
    else:
        return 'High'

def categorize_and_append_states(file_path):
    """Categorize travel times into states and append the states to the CSV file."""
    df = pd.read_csv(file_path)
    
    # Convert travel times to minutes
    df['Travel Minutes'] = df['Travel Time'].apply(convert_to_minutes)
    
    # Define bins for Low, Medium, High using quantiles for each dataset separately
    low_threshold, high_threshold = df['Travel Minutes'].quantile([0.33, 0.66]).tolist()
    
    # Categorize travel times into states
    df['State'] = df['Travel Minutes'].apply(assign_state, args=(low_threshold, high_threshold))
    
    # Save the updated DataFrame back to the CSV file, appending the 'State' column
    df.to_csv(file_path, index=False)

# Example usage
file_path = './FCT_project/data/timeseries/Enn-Bel_10thDec.csv'
categorize_and_append_states(file_path)