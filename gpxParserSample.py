import gpx_parser.gpx_parser as gpx_parser

if __name__ == '__main__':
    
    gpx = gpx_parser.gpx_file('Track_002.gpx')
    
    tracks = gpx.getTracks()
    
    for track in tracks:
        print('Name: ' + track.getTrackname())
        
        track.reduceTrackpointsByDistance()
        
        trackpoints = track.getTrackpoints()

        for trackpoint in trackpoints:
 
            print('    Track point: {}, Lat: {}, Lon: {}, Distance to previous point: {}'.format(trackpoint.time,
                                                                                                 trackpoint.lat,
                                                                                                 trackpoint.lon,
                                                                                                 track.getDistanceToPrevPoint(trkpoint=trackpoint))
                  )
        
        print('\nNumber of track points: {}\nDistance: {}\nmin evelation: {}\nmax. elevation: {}'.format(track.getNumTrackpoints(),
                                                                                                         track.getTrackDistance(),
                                                                                                         *track.getMinMaxElevation())
              )
