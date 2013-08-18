'''
Created on 12.08.2013

@author: mstuebner
'''

import math

class gpx_data:
    
    def get_distance_from_lat_lon(self, lat1, lon1, lat2, lon2):
        """ Uses the Haversine formula for calculations """
        radius = 6371
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(d_lon / 2) * math.sin(d_lon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return d    