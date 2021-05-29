import csv
import numpy as np
import simplekml
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
	return (lat, lon)

def headingchecker(heading):
	if heading[0].upper() != 'N' and heading[0].upper() != 'S':
		print('Syntax error! Make sure you have a "N" or "S" as the first character of your heading.')
	
	if heading[len(heading) - 1].upper() != 'E' and heading[len(heading) - 1].upper() != 'W':
		print('Syntax error! Make sure you have a "E" or "W" as the last character of your heading.')
	
	if len(heading) != 8:
		print('Syntax error! Your heading is the wrong length.')

def createkml(coords):
	kml = simplekml.Kml()
	for lat, lon in coords:
	    pnt = kml.newpoint()
	    pnt.coords = [(lon, lat)]
	kml.save("newpoints.kml")
			


def met2cor(lat, lon, heading, distance):
	angle = bearing2rad(heading)

	p1_cartesian = WGS84toSPCS(lat, lon)

	delta_north = distance * np.cos(angle)
	delta_east = distance * np.sin(angle)

	if heading[0].upper() == 'S':
		delta_north = -delta_north

	if heading[len(heading) - 1].upper() == 'W':
		delta_east = -delta_east

	p2_northing = p1_cartesian[0] + delta_north
	p2_easting = p1_cartesian[1] + delta_east
	
	return SPSCtoWGS84(p2_northing, p2_easting)



with open('points.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	row = list(csv_reader)

	lat = float(row[1][3])
	lon = float(row[1][4])
	coords = [(lat, lon)]
	
	for i in range(len(row)-2):
		coords.append(met2cor(lat, lon, row[i + 2][1], float(row[i + 2][2])))
		lat = coords[i-1][0]
		lon = coords[i-1][1]

with open('newpoints.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter = ',')
#	writer.writerow(row[0])
#	writer.writerow(row[1])
	
	for i in range(len(coords)):
		writer.writerow(coords[i])

print(coords)			
createkml(coords)
