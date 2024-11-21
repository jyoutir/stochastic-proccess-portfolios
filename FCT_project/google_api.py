"""
Block for calling Google Cloud API. 
"""

from api_calls import traffic_data
from datetime import datetime, timedelta


api_key = 'AIzaSyDDIVtSMMLEydyxNg6sjkNw5qLuoxwkdis'  # API key
origin = 'Enniskillen, UK' 
destination = 'Belfast, UK' 

# NOTE:     format - (yr, mnth, day, hr, mins)
start_time = datetime(2024, 11, 25, 0, 0)  

end_time = datetime(2024, 11, 26, 0, 0) 
interval = 10

traffic_data(api_key, origin, destination, start_time, end_time, interval)

