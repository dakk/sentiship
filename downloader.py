import fnmatch
from datetime import date
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter

SUSER = input('user:')
SPASSWORD = input('password:')

sapi = SentinelAPI(SUSER, SPASSWORD, 'https://scihub.copernicus.eu/dhus/')

srd_wkt = """POLYGON((
	8.1298828125 38.5338022218,
	9.9371337891 38.5338022218,
	9.9371337891 41.522056887,
	8.1298828125 41.522056887,
	8.1298828125 38.5338022218
))"""

p = sapi.query(area=srd_wkt, date=('NOW-9DAYS', 'NOW'), area_relation="Intersects", platformname='Sentinel-2',
					processinglevel='Level-2A')
print(p)
#sapi.to_geojson(p)



def path_filter(a):
	npath = a['node_path']
	return fnmatch.fnmatch(npath, '*_TCI_10m.jp2') # or fnmatch.fnmatch(npath, '*_SCL_20m.jp2')

for key, value in p.items():
	size = value['size']
	cov = value['cloudcoverpercentage']
	if cov > 30.:
		print ('skipping for cloud coverage', size, cov)
		continue
	print(size, cov)
	sapi.download(key, './tempdataset', nodefilter=path_filter)