import sys
import xml.etree.ElementTree as ET
import math

if len(sys.argv) < 2:
	print("Usage: gpxtool <gpx file>\n")
	sys.exit(1)

gpx_file = sys.argv[1]
print(f"Loading {gpx_file}...")

tree = ET.parse(gpx_file)
ns = { 'gpx': 'http://www.topografix.com/GPX/1/1' }

trkpts = tree.findall('./gpx:trk/gpx:trkseg/gpx:trkpt', ns)
print(f"Found {len(trkpts)} trackpoints...\n")
if len(trkpts) is 0:
	print("ERROR: No trackpoints found")
	sys.exit(1)

class sph_point:
	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon

s = list(map(lambda x: sph_point(float(x.attrib["lat"]), float(x.attrib["lon"])), trkpts))

class vector3:
	def __init__(self, x: float, y: float, z: float):
		self.x = x
		self.y = y
		self.z = z

	def len(self) -> float:
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

	def scale(self, r):
		self.x *= r
		self.y *= r
		self.z *= r

class cart_point:
	def __init__(self, x: float, y: float, z: float):
		self.x = x
		self.y = y
		self.z = z

	def __init__(self, sph: sph_point):
		lat = math.radians(sph.lat)
		lon = math.radians(sph.lon)
		self.x = math.cos(lon) * math.cos(lat)
		self.y = math.sin(lon) * math.cos(lat)
		self.z = math.sin(lat)

	def __sub__(p, q) -> vector3:
		return vector3(p.x - q.x, p.y - q.y, p.z - q.z)

p = list(map(lambda x: cart_point(x), s))
for v in p:
	print(f"({v.x}, {v.y}, {v.z})")

d = [None] * (len(p) - 1)
radius = 6378.1370 # semi-major axis of WGS84 ellipsoid in km

for i in range(len(d)):
	d[i] = (p[i+1] - p[i])
	d[i].scale(radius)

norms = list(map(lambda x: x.len(), d))

distance = sum(norms)
print(f"Distance = {distance}km")
