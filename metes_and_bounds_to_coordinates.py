from pyproj import Transformer

def deg2dec(heading):
	deg = int(str(heading[1]) + str(heading[2]))
	min = int(str(heading[3]) + str(heading[4]))
	sec = int(str(heading[5]) + str(heading[6]))

	dec = deg + min/60 + sec/3600
	return dec

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

"""
def met2cor(lat, lon):
	transformer = Transformer.from_crs("EPSG:4326", "EPSG:6479", always_xy=True)
	SP_cartesian = transformer.transform(lon, lat)
	EP_lon = SP_cartesian[0] + 0
	EP_lat = SP_cartesian[1] + 10

	transformer = Transformer.from_crs("EPSG:6479", "EPSG:4326", always_xy=True)
	EP_deg = transformer.transform(EP_lon, EP_lat)
	EP_deg = [EP_deg[1], EP_deg[0]]
	print(lat, lon)
	print(EP_deg)
"""

#met2cor(30.485086, -90.927388)

#met2cor('30.485086, -90.927388', 'N001417W', '201.3')

coords = [30.000001, -90.000001]
print(coords)
print(WGS84toSPCS(coords[0], coords[1]))
print(SPSCtoWGS84(547948.1273229495, 3702866.0204362012))
