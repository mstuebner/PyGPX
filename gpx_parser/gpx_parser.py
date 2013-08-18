from xml.dom import minidom
from collections import namedtuple

from gpx_data import gpx_data


gpx_trackpoint = namedtuple('trackpoint',
                            'time, lon, lat, ele'
                            )

gpx_track = namedtuple('track',
                       'name, trackpoints'
                       )


class gpx_file:
    
    def __init__(self, filename):
        self.tracks = []
        try:
            doc = minidom.parse(filename)
            doc.normalize()
        except:
            return
        
        gpx = doc.documentElement
        for node in gpx.getElementsByTagName('trk'):
            self.tracks.append(self.parseTrack(node))
    
    def parseTrack(self, track):

        _trackname = track.getElementsByTagName('name')[0].firstChild.data
        _trackpoints = []
            
        for track_seg in track.getElementsByTagName('trkseg'):
            for track_point in track_seg.getElementsByTagName('trkpt'):
                lat = float(track_point.getAttribute('lat'))
                lon = float(track_point.getAttribute('lon'))
                try:
                    ele = float(track_point.getElementsByTagName('ele')[0].firstChild.data)
                except:
                    ele = 0
                
                try:
                    rfc3339 = track_point.getElementsByTagName('time')[0].firstChild.data
                except:
                    rfc3339 = len(_trackpoints)
                    
                _trackpoints.append(gpx_trackpoint(rfc3339, lon, lat, ele))

        return gpx_track(_trackname, _trackpoints)

    def getTracks(self):
        return self.tracks


class gpx_track:
    
    def __init__(self, trackname, trackpoints):
        self.trackname = trackname
        self.trackpoints = trackpoints
        self.sum_distance = self.getTrackDistance()
        self.num_trackpoints = self.getNumTrackpoints() 
        
    def getTrackname(self):
        return self.trackname

    def getTrackDistance(self):
        old_lat = 0 
        old_lon = 0
        sum_distance = 0
    
        for trackpoint in self.trackpoints:
                
            if old_lat > 0 and old_lon > 0:
                dist = gpx_data.gpx_data().get_distance_from_lat_lon(lat1=old_lat, 
                                                                     lon1=old_lon, 
                                                                     lat2=trackpoint.lat, 
                                                                     lon2=trackpoint.lon)
            else:
                dist = 0
                 
            sum_distance += dist
             
            old_lat = trackpoint.lat
            old_lon = trackpoint.lon

        return sum_distance
    
    def getTrackpoints(self):
        return self.trackpoints

    def getDistanceToPrevPoint(self, trkpoint):
        idx = self.trackpoints.index(trkpoint)
        
        if idx > 0:
            dist = gpx_data.gpx_data().get_distance_from_lat_lon(lat1=self.trackpoints[idx-1].lat, 
                                                                 lon1=self.trackpoints[idx-1].lon, 
                                                                 lat2=trkpoint.lat, 
                                                                 lon2=trkpoint.lon)
            return dist

    def getNumTrackpoints(self):
        return len(self.trackpoints)
    
    def removeTrackpoint(self, trkpoint):
        del self.trackpoints[self.trackpoints.index(trkpoint)]
    
    def reduceTrackpointsByDistance(self, min_distance=0.1):
        for trackpoint in self.trackpoints:
            if self.trackpoints.index(trackpoint) > 0:
                dist = self.getDistanceToPrevPoint(trackpoint)
                if dist < min_distance:
                    self.removeTrackpoint(trackpoint)

    def getMinMaxElevation(self):
        elevation = []
        
        for trackpoint in self.trackpoints:
            elevation.append(trackpoint.ele)
            
        return min(elevation), max(elevation)


if __name__ == '__main__':
    
    gpx = gpx_file('d:\\temp\\Track_002.gpx')
    
    tracks = gpx.getTracks()
    
    for track in tracks:
        print('Name: ' + track.getTrackname())
        
        trackpoints = track.getTrackpoints()
        distance = track.getTrackDistance()

        print('Distance: {}'.format(distance))
    
