"""
Google Maps API Travel Time Data Collector

This script allows you to collect travel time data between two locations using Google Maps API.
It records travel times at regular intervals and saves the data to a CSV file.

Prerequisites:
You need a Google Cloud API key. To do this, go to:
# Go to https://cloud.google.com/
# Create a project
# Enable the Directions API
# Create credentials (API key)
"""

from datetime import datetime, timedelta
import os
import csv

# ============== Change the information in this block ==============

# Your Google Cloud API key (Replace this with your own key)
api_key = 'YOUR API KEY GOES HERE'

# Set your origin and destination points
origin = 'Enniskillen, UK' 
destination = 'Belfast, UK' 

# NOTE:     format - (yr, mnth, day, hr, mins). Set your time range for data collection.
start_time = datetime(2024, 11, 25, 0, 0)  
end_time = datetime(2024, 11, 26, 0, 0)   

# Set how often to collect data (in minutes)
interval = 10 

# SET the location where the file is saved. Change this to your preferred save location
# e.g., for Windows: save_directory = "C:/Users/YourName/Desktop"
save_directory = "."  



# ==== no need to alter anything below this. Feel free to use AI to understand this  =======

def traffic_data(api_key, origin, destination, start_time, end_time, interval, save_directory="."):
    """
    Collects traffic data using Google Maps API and saves it to a CSV file.
    
    Parameters:
        api_key (str): Your Google Cloud API key
        origin (str): Starting location
        destination (str): Ending location
        start_time (datetime): When to start collecting data
        end_time (datetime): When to stop collecting data
        interval (int): Minutes between each data collection
        save_directory (str): Where to save the output file (defaults to current directory)
    """
    current_time = start_time
    data_rows = []

    print(f"Starting data collection from {origin} to {destination}")
    print(f"Time range: {start_time} to {end_time}")
    
    while current_time <= end_time:
        timestamp = int(current_time.timestamp())
        url = (
            "https://maps.googleapis.com/maps/api/directions/json"
            f"?origin={origin}&destination={destination}&departure_time={timestamp}&key={api_key}"
        )
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['status'] == 'OK':
                leg = data['routes'][0]['legs'][0]
                duration_in_traffic = leg.get('duration_in_traffic', {}).get('text', 'NOT FOUND')
                print(f"Travel time at {current_time}: {duration_in_traffic}")
                data_rows.append([current_time.strftime("%Y-%m-%d %H:%M:%S"), duration_in_traffic])
            else:
                print(f"Error in response: {data['status']}. Details: {data.get('error_message', 'No additional details')}")
        else:
            print(f"Request failed with status code: {response.status_code}")
        
        current_time += timedelta(minutes=interval)
    
    filename = f"{origin[:3]}-{destination[:3]}_{start_time.strftime('%dth%b_%H-%M')}.csv"
    filepath = os.path.join(save_directory, filename)
    
    try:
        # create directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)
        
        # save collected data to CSV file
        with open(filepath, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date and Time', 'Travel Time'])
            csvwriter.writerows(data_rows)
        
        print(f"\nData collection completed!")
        print(f"Data saved to: {os.path.abspath(filepath)}")
        
    except PermissionError:
        print(f"\nError: No permission to write to {save_directory}")
        print("Please choose a different save location or run with appropriate permissions")
    except Exception as e:
        print(f"\nError saving file: {str(e)}")
        print("Please check your save location and try again")

if __name__ == "__main__":
    traffic_data(api_key, origin, destination, start_time, end_time, interval, save_directory)