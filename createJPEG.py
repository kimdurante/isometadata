#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from descartes import PolygonPatch
import matplotlib.pyplot as plt 
import shapefile
import os
import sys
from PIL import Image
import base64

def get_cmap(n, name='hsv'):
  '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
  RGB color; the keyword argument name must be a standard mpl colormap name.'''
  return plt.cm.get_cmap(name, n)

def createJPEG():
    shapefile_name = os.path.join(dirName, f)
    metadata = os.path.join(dirName, f + '.xml')
    tree = ET.parse(metadata)
    root = tree.getroot()
    thumbnail = root.find('Binary/Thumbnail/Data') 
    outputfile = shapefile_name[:-4] + '.jpg'
    polys  = shapefile.Reader(shapefile_name)
    shapes = polys.shapes()
    cmap   = get_cmap(len(shapes))
    fig = plt.figure()
    fig.set_size_inches(30, fig.get_figheight(), forward=True)
    #DPI = fig.get_dpi()
    print (f)
    ax  = fig.add_axes((0,0,1,1))
    for i,poly in enumerate(shapes):
        poly  = poly.__geo_interface__
        color = cmap(i)
        ax.add_patch(PolygonPatch(poly, fc=None, ec="black", alpha=1, zorder=2))
        ax.axis('scaled')
        ax.set_axis_off()
        plt.savefig(outputfile, bbox_inches='tight', pad_inches=0)
        with open(outputfile, "rb") as image:
            b64string = base64.b64encode(image.read())
            #thumbnail.clear()
            thumbnail.text = str(b64string)[2:]
            tree.write(metadata)

            
for dirName, subDirs, fileNames in os.walk('.'):
    for f in fileNames:
        if f.startswith('.'):
            continue
        if f.endswith('.shp'):
            createJPEG()
