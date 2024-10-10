"""
This is code for all API requssts. 
"""

import requests

def get_traffic_data(api_key, origin, destination):
    url = (
        "https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&departure_time=now&key={api_key}"
    )
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['status'] == 'OK':
            leg = data['routes'][0]['legs'][0]
            # Use 'duration_in_traffic' if available, otherwise fallback to 'duration'
            duration = leg.get('duration_in_traffic', leg['duration'])['text']
            print(f"ERROR: TRAFFIC DATA NOT FETCHED. Travel time (0 TRAFFIC): {duration}")
        else:
            print(f"Error in response: {data['status']}")
    else:
        print(f"Request failed with status code: {response.status_code}")