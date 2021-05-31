import csv
import numpy as np
import simplekml
from pyproj import Transformer
import pprint

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

def createkml(points):
	kml = simplekml.Kml()
	for i in range(len(points)):
		pnt = kml.newpoint(name = points[i]['Name'], coords = [(points[i]['WGS84longitude'], points[i]['WGS84latitude'])])
		pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
	kml.save("newpoints.kml")
	print('KML exported succesfully.')


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

def loadmeetsandbounds(filename):
	with open(filename, 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		points = list(csv_reader)
		return points

def exportWGS84(listofdicts):
	with open('newpoints.csv', 'w', newline='') as csvfile:
		fieldnames = listofdicts[0].keys()
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(len(listofdicts)):
			writer.writerow(listofdicts[i])
		print('CSV exported succesfully.')

def errordist():
	POB = WGS84toSPCS(points[0]['WGS84latitude'], points[0]['WGS84longitude'])
	END = WGS84toSPCS(points[len(points) - 1]['WGS84latitude'], points[len(points) - 1]['WGS84longitude'])
	north_err = (END[0] - POB[0]) * 12
	east_err = (END[1] - POB[1]) * 12
	total_error = np.sqrt(north_err**2 + east_err**2)
	print('Closed-loop descrepancy of ' + str('{0:.2g}'.format(north_err)) + ' inches north and ' + str('{0:.2g}'.format(east_err)) + ' inches east.')
	print('Total error is: ' + str('{0:.2g}'.format(total_error)) + ' inches.')







points = loadmeetsandbounds('points.csv')

for i in range(len(points) - 1):
	coords = (met2cor(points[i]['WGS84latitude'], points[i]['WGS84longitude'], points[i]['Heading'], float(points[i]['Distance'])))
	points[i + 1]['WGS84latitude'] = coords[0]
	points[i + 1]['WGS84longitude'] = coords[1]
	print(coords)


EOB = met2cor(points[len(points)-1]['WGS84latitude'], points[len(points)-1]['WGS84longitude'], points[len(points)-1]['Heading'], float(points[len(points)-1]['Distance']))
points.append({'WGS84latitude': EOB[0], 'WGS84longitude': EOB[1], 'Name': 'EOB'})



#pprint.pprint(points)


exportWGS84(points)
createkml(points)
errordist()
