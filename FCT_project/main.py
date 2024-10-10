"""
This is MAIN code for FCT PROJECT. Here we call Google API. 
"""

import os
from api_calls import get_traffic_data


api_key = 'AIzaSyDDIVtSMMLEydyxNg6sjkNw5qLuoxwkdis'  # API key
origin = 'New York, NY'  
destination = 'Los Angeles, CA'  

get_traffic_data(api_key, origin, destination)

