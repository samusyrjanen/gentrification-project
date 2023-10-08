# Convert the Helsingi region postal code region data into
# a valid FeatureCollection.
#
# Boundary data as a shapefile can be obtained from:
#
# https://hri.fi/data/fi/dataset/paakaupunkiseudun-postinumeroalueet/resource/617718ea-dcba-4ae0-a928-4b9642df76cf
#

import geopandas as gpd
import io
import os
import requests
import sys
import zipfile

u = 'https://avoidatastr.blob.core.windows.net/avoindata/AvoinData/9_Kartat/PKS%20postinumeroalueet/Shp/PKS_postinumeroalueet_2023_shp.zip'
s = u.split('/')[-1:][0]
o = '.'.join(s.split('.')[:-1]) + '.json'

r = requests.get(u)
r.raise_for_status()

b = io.BytesIO(r.content)
if not zipfile.is_zipfile(b):
    print(f'{u} does not contain a ZIP file.', file = sys.stderr)
    sys.exit(1)

z = zipfile.ZipFile(b)
z.extractall()

j = gpd.read_file(s).to_json(to_wgs84 = True)
with open(o, 'w') as geojson:
    geojson.write(j)

for _ in z.namelist():
    os.remove(_)

# end of file.