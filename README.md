# GeoDownloader

Python little functions to make high resolution map. From IGN/Geoportail data.

[IGN Tool to identify tile coordinates according to zoom level](https://geoservices.ign.fr/documentation/services/api-et-services-ogc/images-tuilees-wmts-ogc#1586)

Made with Python 3.7.4

## Example

```
import geoDownloader

"""
    Little script to make high resolution map. Specifically here it is a blend
    between satellite images and topography IGN map. 

    Below a link to a tool to identify the tile COL/ROW of the top left of the map 
    according to the zoom level
 
    https://geoservices.ign.fr/documentation/services/api-et-services-ogc/images-tuilees-wmts-ogc#1586
"""

map_size = 10
col      = 33323
row      = 24053
zoom     = 16

layer1 = "ORTHOIMAGERY.ORTHOPHOTOS"
layer2 = "GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN25TOUR.CV"

print("Starting satellite download")
geoDownloader.save_map(map_size,col,row,zoom,layer1)
print("Starting map download")
geoDownloader.save_map(map_size,col,row,zoom,layer2)
print("Blending maps")
geoDownloader.blend_maps(layer2+"/final.jpg",layer1+"/final.jpg","final.png",0.4)
print("Done")
```

## Result

![resulting image](final.png)

## To do

-[ ] delete tiles after final rendering

-[ ] add console arguments for map size , coordinates , zoom

-[ ] take coordinates as argument
