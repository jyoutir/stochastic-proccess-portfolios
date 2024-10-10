"""
This is code for all API requssts. 
"""
import csv
import requests
from datetime import datetime, timedelta

def traffic_data(api_key, origin, destination, start_time, end_time, interval):
    current_time = start_time
    data_rows = []

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
    
    filename = f"{origin[:3]}-{destination[:3]}_{start_time.strftime('%dth%b')}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date and Time', 'Travel Time'])
        csvwriter.writerows(data_rows)
    
    print(f"Data saved to {filename}")