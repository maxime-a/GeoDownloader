"""
    11/01/23 --- Maxime Ay
    
    Little functions to help making of maps from tiles of IGN services.
    
    IGN documentation :
    https://geoservices.ign.fr/documentation/services/api-et-services-ogc/images-tuilees-wmts-ogc#1586
"""

from PIL import Image
import os
import urllib.request

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print("\n")

def download_tile(x,y,z,layer,url):
    """ Download a tile from IGN service

    Parameters
    ----------
    x : int, col index of the tile
    
    y : int, col index of the top left tile
    
    z : int, zoom level

    layer : str, name of the map type from IGN api

    url : str, url to be formatted with previous data
    
    """
    
    req = urllib.request.Request(
            url.format(layer=layer,x=x,y=y,z=z), 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

    f = urllib.request.urlopen(req)

    return f

def save_tile_as_jpg(f,path):
    """ Save a binary to jpg

    Parameters
    ----------
    f : binary, jpg binary of a tile
    
    path : str, path with included filename 
    
    """
    
    # Open file in binary write mode
    binary_file = open(path, "wb")
    # Write bytes to file
    binary_file.write(f.read())
    # Close file
    binary_file.close()


def save_map(mapSize,xBase,yBase,zoom,layer):
    """ Save a map from IGN api 

    All tiles before being gathred together are downloaded in a folder ./layer

    Parameters
    ----------
    mapSize : int, number of tiles for the sides of the square map
    
    xBase : int, col index of the top left tile
    
    yBase : int, xBase : int, col index of the top left tile

    zoom : int, zoom level 

    layer : str, name of the map type from IGN api
    
    """

    try:
        os.mkdir(layer)
    except OSError as error:
        print("Directory already created, same will be used")

    url = "https://wxs.ign.fr/an7nvfzojv5wa96dsga5nk8w/geoportail/wmts?layer={layer}&style=normal&tilematrixset=PM&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image/jpeg&TileMatrix={z}&TileCol={x}&TileRow={y}"

    tiles = []
    
    #download all tiles
    for j in range(mapSize):
        for i in range(mapSize):
            z = zoom
            x = xBase + i
            y = yBase + j

            advancement = (j*mapSize+i+1) / (mapSize**2)
            printProgressBar(advancement, 1, prefix = 'Progress:', suffix = 'Complete', length = 50)
            f = download_tile(x,y,z,layer,url)
            
            filename=layer+"/tile_{x}_{y}_{z}_{layer}.jpg"
            filename=filename.format(x=x,y=y,z=z,layer=layer)
            save_tile_as_jpg(f,filename)
            tiles.append(filename)

    # Taille des tuiles
    tile_size = (256, 256)

    # Nombre de tuiles par ligne/colonne
    tiles_per_row = mapSize

    # Taille de l'image finale
    final_image_size = (tile_size[0] * tiles_per_row, tile_size[1] * tiles_per_row)

    # Chargement des tuiles
    tile_images = [Image.open(tile) for tile in tiles]

    # Création de l'image finale
    final_image = Image.new("RGB", final_image_size)

    # Ajout des tuiles à l'image finale
    for y in range(tiles_per_row):
        for x in range(tiles_per_row):
            final_image.paste(tile_images[y * tiles_per_row + x], (x * tile_size[0], y * tile_size[1]))

    # Enregistrement de l'image finale
    final_image.save(layer+"/final.jpg")

def blend_maps(path1,path2,pathOutput,opacity):
    """ Blend to images with a specified opacity level

    The image pointed in path1 will be on top with the opacity reduced

    Parameters
    ----------
    path1 : str, path to image1 as jpg
    
    path2 : str, path to image1 as jpg
    
    pathOutput : str, path to output image, the output is a PNG file.

    opacity : float, opacity level, 1.0 is no transparency ,0.0 is total transparency

    Raises
    ------
    SizeError
    If the two images don't have the same sizes
    
    """
    
    # Ouverture des images
    image1 = Image.open(path1)
    image2 = Image.open(path2)

    image1 = image1.convert('RGBA')
    image2 = image2.convert('RGBA')

    if image1.size != image2.size :
        raise SizeError('Size error : images must have the same size')
    
    # Réglage de l'opacité de l'image 1 à 30%
    image1 = Image.blend(image1, Image.new('RGBA', image1.size, (0,0,0,0)), alpha=opacity)
    #image1.putalpha(180)

    # Superposition des images
    result = Image.alpha_composite(image2, image1)

    # Enregistrement de l'image résultante
    result.save(pathOutput)
