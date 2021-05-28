import numpy as np
from pyproj import Transformer

def bearing2rad(heading):
	deg = int(str(heading[1]) + str(heading[2]))
	min = int(str(heading[3]) + str(heading[4]))
	sec = int(str(heading[5]) + str(heading[6]))

	rad = np.radians(deg + min/60 + sec/3600)
	return rad

def WGS84toSPCS (lat, lon):
	transformer = Transformer.from_crs("EPSG:4326", "EPSG:6479", always_xy=True)
	cartesian = transformer.transform(lon, lat)
	east = cartesian[0]
	north = cartesian[1]
	return [north, east]

def SPSCtoWGS84 (north, east):
	transformer = Transformer.from_crs("EPSG:6479", "EPSG:4326", always_xy=True)
	latlong = transformer.transform(east, north)
	lat = latlong[1]
	lon = latlong[0]
	return [lat, lon]

def met2cor(lat, lon, heading, distance):
	angle = bearing2rad(heading)

	SPSC = WGS84toSPCS(lat, lon)
	p1_northing = SPSC[0]
	p1_easting = SPSC[1]
	
	p2_northing = p1_northing + (distance * np.cos(angle))
	p2_easting = p1_easting + (distance * np.sin(angle))

	return SPSCtoWGS84(p2_northing, p2_easting)

coords = [30.485086, -90.927388]
print(coords)
print(met2cor(coords[0], coords[1], 'N001417W', 201.3))


#met2cor('30.485086, -90.927388', 'N001417W', '201.3')

