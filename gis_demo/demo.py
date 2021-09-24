import arcgis
from arcgis.gis import GIS
import pandas as pd
from arcgis.geocoding import Geocoder, get_geocoders, geocode

gis = GIS("https://www.arcgis.com", "arcgis_python", "P@ssword123")
mymap = gis.map()
mymap.basemap = "osm"

results = geocode('北京市海淀区莲花池西路国家测绘地理信息局')
pd.DataFrame(results)

for res in results:
    popup = {
        "title": res["attributes"]["Region"],
        "content": "address:" + res["address"]
    }
    mymap.draw(res, popup=popup)