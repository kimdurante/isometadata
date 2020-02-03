import csv
import os
import xml.etree.ElementTree as ET


attrdict = {}
reader = csv.reader(open("attributes.csv", "r"))
for rows in reader:
    label = rows[0]
    definition = rows[1] 
    attrdict[label] = definition


for dirName, subDirs, fileNames in os.walk('.'):
    for f in fileNames:
        if f.endswith('shp.xml'):
            print (f)
            file = os.path.join(dirName, f)
            tree = ET.parse(file)
            root = tree.getroot()
            atts = root.findall('eainfo/detailed/attr')
            alabel = root.findall('eainfo/detailed/attr/attrlabl')
            ascale = root.findall('eainfo/detailed/attr/attscale')
            for i in atts:
                attlabel = i[0].text
                for k,v in attrdict.items():
                    if attlabel == k:
                       i.insert(6,ET.Element('attrdef'))
                       i[6].text = v
                       print (i[6].tag, i[6].text)
                       tree.write(file)


                
