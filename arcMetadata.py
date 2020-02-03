import xml.etree.ElementTree as ET
import os
from datetime import datetime
import time
import csv
template = 'templates/template_arc.xml'


#Create a dictionary entry containing metadata for each layer
metadict = {}
reader = csv.reader(open('metadata.csv', 'r'))
#skip first line (header row)
next(reader)
for rows in reader:
    filename = rows[0]
    srs = rows[1]
    geomType = rows[2]
    westbc = rows[3]
    southbc = rows[4]
    eastbc = rows[5]
    northbc = rows[6]
    fileFormat = rows[7]
    identifier = rows[8]
    title = rows[9]
    description = rows[10]
    originator = rows[11]
    publisher = rows[12]
    issueDate = rows[13]
    temporal = rows[14]
    subjects = rows[15].split('|')
    topicCat = rows[16]
    spatialSubjects = rows[17].split('|')
    fcUUID = rows[18]
    language = rows[19]
    collTitle = rows[20]
    collId = rows[21]
    access = rows[22]
    usageRights = rows[23]
    metadict[filename] = srs, geomType, westbc, southbc, eastbc, northbc, fileFormat, identifier, title, description, originator, publisher, issueDate, temporal, subjects, topicCat, spatialSubjects, fcUUID, collTitle, collId, access, usageRights, language
    
    
def applyTemplate():
    tree = ET.parse(template)
    root = tree.getroot()
    new_file = filePath + '.xml'
    tree.write(new_file)

def addMetadata():
    for k, v in metadict.items():
        if k + '.xml' == f:
            distName.text = k
            URL.text = 'https://purl.stanford.edu/' + v[7]
            dataSetURI.text = 'https://purl.stanford.edu/' + v[7]
            resTitle.clear()
            resTitle.text = v[8]
            abstract.clear()
            abstract.text = v[9]
            geom_type = v[3]
            metadataID.text = 'edu.stanford.purl:' + v[7]
            temporal = datetime.strptime(v[13], '%m/%d/%y')
            temporal = datetime.strftime(temporal,'%Y-%m-%dT%H:%M:%S')
#            tempExtent.text = v[13] + 'T00:00:00'
            tempExtent.text = temporal
            publisher.text = v[11]
            issueDate = datetime.strptime(v[12], '%m/%d/%y')
            issueDate = datetime.strftime(issueDate,'%Y-%m-%dT%H:%M:%S')
            pubDate.text = issueDate
            year = pubDate.text[:4]
            fcID.text = v[17]
            distURL.text = 'https://purl.stanford.edu/' + v[7]
            collectionTitle.text = v[18]
            collectionId.text = 'https://purl.stanford.edu/' + v[19]
            rightsText.text = v[21]
            themeKey.text = v[14][0]
            placeKey.text = v[16][0]
            credit.text = v[11] + '. (' + year + '). ' + v[8] + '. Available at: https://purl.stanford.edu/' + v[7]
            for index, theme in enumerate(v[14][0:]):
                if index > 0:
                    themeKeys.insert(index, ET.Element('keyword'))
                    themeKeys[index].text = theme
            for index, place in enumerate(v[16][0:]):
                if index > 0:
                    placeKeys.insert(index, ET.Element('keyword'))
                    placeKeys[index].text = place
            tree.write(filePath)
                        
    
#walk through the directory and find shapefiles
for dirName, subDirs, fileNames in os.walk('./data'):
    for f in fileNames:
        if f.endswith('.shp'):
            filePath = os.path.join(dirName, f)
            applyTemplate()
        if f.endswith(".shp.xml"):
            print (f)
            filePath = os.path.join(dirName, f)
            tree = ET.parse(filePath)
            root = tree.getroot()
            dataIdInfo = root.find('dataIdInfo')
            metadataID = root.find('mdFileID')
            dataSetURI = root.find('dataSetURI')
            resTitle = root.find('dataIdInfo/idCitation/resTitle')
            abstract = root.find('dataIdInfo/idAbs')
            placeKeys = root.find('dataIdInfo/placeKeys')
            placeKey = root.find('dataIdInfo/placeKeys/keyword')
            themeKeys = root.find('dataIdInfo/themeKeys')
            themeKey = root.find('dataIdInfo/themeKeys/keyword')
            pubDate = root.find('dataIdInfo/idCitation/date/pubDate')
            contactName = root.find('dataIdInfo/idPoC/rpOrgName')
            address = root.find('dataIdInfo/idPoC/rpCntInfo/cntAddress/eMailAdd')
            tempExtent = root.find('dataIdInfo/dataExt/tempEle/TempExtent/exTemp/TM_Instant/tmPosition')
            distURL = root.find('distInfo/distTranOps/onLineSrc/linkage')
            distName = root.find('distInfo/distTranOps/onLineSrc/orName')
            URL = root.find('dataIdInfo/idCitation/citId/identCode')
            fcID = root.find('contInfo/FetCatDesc/catCitation/citId/identCode')
            fcDate = root.find('contInfo/FetCatDesc/catCitation/date')
            geomObjType = root.find('spatRepInfo/VectSpatRep/geometObjs/geoObjTyp/GeoObjTypCd')
            credit = root.find('dataIdInfo/idCredit')
            collectionTitle = root.find('dataIdInfo/aggrInfo/aggrDSName/resTitle')
            collectionId = root.find('dataIdInfo/aggrInfo/aggrDSName/citId/identCode')
            rightsText = root.find('dataIdInfo/resConst/LegConsts/othConsts')
            publisher = root.find('dataIdInfo/idCitation/citRespParty/rpOrgName')
            addMetadata()            
