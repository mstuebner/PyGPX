import gpx_parser.gpx_parser as gpx_parser

if __name__ == '__main__':
    
    gpx = gpx_parser.gpx_parser('Track_002.gpx')
    
    tracks = gpx.getTracks()
    
    for trackname in tracks:
        print('Name: ' + trackname)
        
        gpx.reduceTrackpointsByDistance(name=trackname)
        
        trackpoints = gpx.getTrackpoints(name=trackname)
        sum_distance = gpx.getTrackDistance(name=trackname)

        for trackpoint in trackpoints:

            dist = gpx.getDistanceToPrevPoint(name=trackname, trkpoint=trackpoint)

            print('    Track point: {}, Lat: {}, Lon: {}, Distance to previous point: {}'.format(trackpoint.time,
                                                                                                 trackpoint.lat,
                                                                                                 trackpoint.lon,
                                                                                                 dist)
                  )
            
        print('\nNumber of track points: {}\nDistance: {}'.format(gpx.getNumTrackpoints(trackname),
                                                                sum_distance))
