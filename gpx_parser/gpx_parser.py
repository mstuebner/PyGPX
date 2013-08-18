from xml.dom import minidom
from collections import namedtuple

from gpx_data import gpx_data


gpx_trackpoint = namedtuple('trackpoint',
                            'time, lon, lat, ele'
                            )

gpx_track = namedtuple('track',
                       'name, trackpoints'
                       )


class gpx_parser:
    
    def __init__(self, filename):
        self.tracks = {}
        try:
            doc = minidom.parse(filename)
            doc.normalize()
        except:
            return
        
        gpx = doc.documentElement
        for node in gpx.getElementsByTagName('trk'):
            self.parseTrack(node)
    
    def parseTrack(self, track):
        
        name = track.getElementsByTagName('name')[0].firstChild.data
        
        if not name in self.tracks:
            self.tracks[name] = []
            
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
                    #self.tracks[name][rfc3339]={'lat':lat, 'lon':lon, 'ele':ele}
                except:
                    rfc3339 = len(self.tracks[name])
                    #self.tracks[name][len(self.tracks[name])]={'lat':lat, 'lon':lon, 'ele':ele}
                    
                self.tracks[name].append(gpx_trackpoint(rfc3339, lon, lat, ele))
                        
    def getTrackpoints(self, name):
        trackpoints = self.tracks[name]
        return trackpoints

    def getTrackDistance(self, name):
        trackpoints = self.getTrackpoints(name)
        old_lat = 0 
        old_lon = 0
        sum_distance = 0
    
        for trackpoint in trackpoints:
                
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
    
    def getDistanceToPrevPoint(self, name, trkpoint):
        trackpoints = self.getTrackpoints(name)
        idx = trackpoints.index(trkpoint)
        
        if idx > 0:
            dist = gpx_data.gpx_data().get_distance_from_lat_lon(lat1=trackpoints[idx-1].lat, 
                                                                 lon1=trackpoints[idx-1].lon, 
                                                                 lat2=trkpoint.lat, 
                                                                 lon2=trkpoint.lon)
            return dist

    def getTracks(self):
        return self.tracks
    
    def getNumTrackpoints(self, name):
        return len(self.getTrackpoints(name))
    
    def removeTrackpoint(self, name, trkpoint):
        trackpoints = self.getTrackpoints(name)
        del trackpoints[trackpoints.index(trkpoint)]
    
    def reduceTrackpointsByDistance(self, name, min_distance=0.5):
        trackpoints = self.getTrackpoints(name)
        
        for trackpoint in trackpoints:
            if trackpoints.index(trackpoint) > 0:
                dist = self.getDistanceToPrevPoint(name, trackpoint)
                if dist < min_distance:
                    self.removeTrackpoint(name, trackpoint)

if __name__ == '__main__':
    
    gpx = gpx_parser('d:\\temp\\Track_002.gpx')
    
    tracks = gpx.getTracks()
    
    for track in tracks:
        print('Name: ' + track)
        
        trackpoints = gpx.getTrackpoints(name=track)
        distance = gpx.getTrackDistance(name=track)

        print('Distance: {}'.format(distance))
    
