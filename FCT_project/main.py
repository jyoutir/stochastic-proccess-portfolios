"""
This is MAIN code for FCT PROJECT. Here we call Google API. 
"""

import os
import csv
from api_calls import traffic_data
from datetime import datetime, timedelta


api_key = 'AIzaSyDDIVtSMMLEydyxNg6sjkNw5qLuoxwkdis'  # API key
origin = 'Enniskillen, UK'  
destination = 'Belfast, UK'  

# format : (yr, mnth, day, hr, mins)
start_time = datetime(2025, 12, 25, 0, 0)  
end_time = datetime(2025, 12, 26, 0, 0) 
interval = 10

# historical
traffic_data(api_key, origin, destination, start_time, end_time, interval)

