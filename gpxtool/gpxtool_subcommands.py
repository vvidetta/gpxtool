import xml.etree.ElementTree as ET
import math
import numpy as np
import numpy.linalg as LA

_radius_ = 6378137.0 # semi-major axis of WGS84 ellipsoid in m

class earth_coord:
	def __init__(self, ele: float, lat: float, lon: float):
		"""
		ele is in metres.
		lat and lon are in degrees.
		"""
		self.ele = ele
		self.lat = lat
		self.lon = lon

class cart_point:
	def __init__(self, sph: earth_coord):
		lat = math.radians(sph.lat)
		lon = math.radians(sph.lon)
		r = _radius_ + sph.ele
		self.x = r * math.cos(lon) * math.cos(lat)
		self.y = r * math.sin(lon) * math.cos(lat)
		self.z = r * math.sin(lat)

	def __sub__(p, q) -> np.array:
		return np.array([p.x - q.x, p.y - q.y, p.z - q.z])

def _get_trackpoints(gpx_file: str) -> list:
	print(f"Loading {gpx_file}...")

	tree = ET.parse(gpx_file)
	ns = { 'gpx': 'http://www.topografix.com/GPX/1/1' }

	trkpts = tree.findall('./gpx:trk/gpx:trkseg/gpx:trkpt', ns)
	print(f"Found {len(trkpts)} trackpoints...")
	if len(trkpts) is 0:
		print("ERROR: No trackpoints found")
		raise Exception()

	return list(map(lambda x: earth_coord(float(x.find('gpx:ele', ns).text), float(x.attrib["lat"]), float(x.attrib["lon"])), trkpts))

def distance(gpx_file: str):
	p = _get_trackpoints(gpx_file)

	distance = 0
	for i in range(len(p) - 1):
		distance += LA.norm(cart_point(p[i+1]) - cart_point(p[i]))

	print(f"Distance = {distance}m")

def top(gpx_file: str):
	p = _get_trackpoints(gpx_file)

	top = p[0]
	for i in range(1, len(p)):
		if p[i].ele > top.ele:
			top = p[i]

	print(f"Top of the ride @ ({top.lat}, {top.lon}), Elevation {top.ele}m")

def north(gpx_file: str):
	p = _get_trackpoints(gpx_file)

	north = p[0]
	for i in range(1, len(p)):
		if p[i].lat > north.lat:
			north = p[i]

	print(f"Northernmost point @ ({north.lat}, {north.lon})")

