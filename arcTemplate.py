#applyTemplate.py

import xml.etree.ElementTree as ET
import os

template = 'templates/template_arc.xml'
#copy template to new file named for each layer
def applyTemplate():
    tree = ET.parse(template)
    root = tree.getroot()
    new_file = filePath + '.xml'
    tree.write(new_file)
    print (f)
    
#walk through the directory and locate shapefiles
for dirName, subDirs, fileNames in os.walk('.'):
    for f in fileNames:
        if f.endswith('.shp'):
            filePath = os.path.join(dirName, f)
            applyTemplate()
