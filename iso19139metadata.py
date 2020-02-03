import csv
import os
from datetime import datetime
import xml.etree.ElementTree as ET

#Map and register namespaces

namespaces = {'gmd': 'http://www.isotc211.org/2005/gmd','gco': 'http://www.isotc211.org/2005/gco', 'gml': 'http://www.opengis.net/gml', 'gfc': 'http://www.isotc211.org/2005/gfc'}
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
ET.register_namespace('gmd', 'http://www.isotc211.org/2005/gmd')
ET.register_namespace('gco', 'http://www.isotc211.org/2005/gco')
ET.register_namespace('gts', 'http://www.isotc211.org/2005/gts')
ET.register_namespace('gss', 'http://www.isotc211.org/2005/gss')
ET.register_namespace('gsr', 'http://www.isotc211.org/2005/gsr')
ET.register_namespace('gfc', 'http://www.isotc211.org/2005/gfc')
ET.register_namespace('gmx', 'http://www.isotc211.org/2005/gmx')
ET.register_namespace('gmi', 'http://www.isotc211.org/2005/gmi')
ET.register_namespace('gml', 'http://www.opengis.net/gml')
idinfo = 'gmd:identificationInfo/gmd:MD_DataIdentification/'
citeinfo = 'gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/'
distinfo = 'gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/'


##Create a dictionary of metadata values ('metadict') from metadata.csv

metadict = {}
reader = csv.reader(open('metadata.csv', 'r'))
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
    #description = rows[10].decode('latin-1')
    metadict[filename] = srs, geomType, westbc, southbc, eastbc, northbc, fileFormat, identifier, title, description, originator, publisher, issueDate, temporal, subjects, topicCat, spatialSubjects, fcUUID, collTitle, collId, access, usageRights, language

def deleteElements():
    for index, tkw in enumerate(themeKeywords):
        if index > 0:
            del_key = md_themeKeywords[0].find('{http://www.isotc211.org/2005/gmd}keyword')
            md_themeKeywords[0].remove(del_key)
    for index, pkw in enumerate(placeKeywords):
        if index > 0:
            del_key = md_placeKeywords[0].find('{http://www.isotc211.org/2005/gmd}keyword')
            md_placeKeywords[0].remove(del_key)
    for index, langs in enumerate(language):
        if index > 0:
            del_key = root[12][0].find('{http://www.isotc211.org/2005/gmd}language[0]')
            root[12][0].remove(del_key)           
    
def createMetadata():
    for k, v in metadict.items():
        if k[:-4] == f[:-4]:
            metadataID.text = 'edu.stanford.purl:' + v[7]
            URL.text = 'https://purl.stanford.edu/' + v[7]
            URI.text = 'https://purl.stanford.edu/' + v[7]
            distURL.text = 'https://purl.stanford.edu/' + v[7]
            distName.text = k
            title.text = v[8]
            mdDateStamp.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            #deleteElements()
            temporal = datetime.strptime(v[13], '%m/%d/%y')
            temporal = datetime.strftime(temporal,'%Y-%m-%dT%H:%M:%S')
            tempInstant.text = temporal
            issueDate = datetime.strptime(v[12], '%m/%d/%y')
            issueDate = datetime.strftime(issueDate,'%Y-%m-%d')
            date.text = issueDate
            year = date.text[:4]
            fcID.text = v[17]
            collection.text = v[18]
            collectionID.text = 'https://purl.stanford.edu/' + v[19]
            for name in publisher:
                name.text = v[11]
                name = name.text
            topicCategory.text = v[15].lower()
            themeKeyword.text = v[14][0]
            placeKeyword.text = v[16][0]
            abstract.text = v[9]
            #root[12][0][8][0].set('codeListValue',v[22])
            language[0].set('codeListValue',v[22])
#             for theme in v[11][1:]:
#                 md_themeKeywords[0].insert(0,ET.Element('{http://www.isotc211.org/2005/gmd}keyword'))
#                 new_themeKeyword = ET.SubElement(md_themeKeywords[0][0],'{http://www.isotc211.org/2005/gco}CharacterString')
#                 new_themeKeyword.text = theme
#             for place in v[5][1:]:
#                 md_placeKeywords[0].insert(0,ET.Element('{http://www.isotc211.org/2005/gmd}keyword'))
#                 new_placeKeyword = ET.SubElement(md_placeKeywords[0][0],'{http://www.isotc211.org/2005/gco}CharacterString')
#                 new_placeKeyword.text = place
#             for lang in v[8][1:]:
#                 root[12][0].insert(9,ET.Element('{http://www.isotc211.org/2005/gmd}language'))
#                 new_lang = root[12][0][9]
#                 new_langCode = ET.SubElement(new_lang,'{http://www.isotc211.org/2005/gmd}LanguageCode')
#                 new_langCode.set('codeList','http://www.loc.gov/standards/iso639-2/')
#                 new_langCode.set('codeSpace','ISO639-2')
#                 new_langCode.set('codeListValue',lang)
            distFormat.text = v[6]
            if geomType == 'Line String':
                geomTypeCode.attrib['codeListValue'] = 'curve'
            if geomType == 'Point':
                geomTypeCode.attrib['codeListValue'] = 'point'
            if geomType == 'Polygon':
                geomTypeCode.attrib['codeListValue'] = 'surface'   
            west.text = v[2]
            east.text = v[4]
            north.text = v[5]
            south.text = v[3]
            auth.text = v[0]
            code.text = 'EPSG'
            rights.text = v[21]
            credit.text = v[11] + '. (' + year + '). ' + v[8] + '. Available at: https://purl.stanford.edu/' + v[7]
            #edition.clear()
            #new_edition = ET.SubElement(citation[2],'{http://www.isotc211.org/2005/gco}CharacterString')
            tree.write(file)

####Walk through a directory of files, find XML documents. Find target metadata elements.
                
for dirName, subDirs, fileNames in os.walk('./data'):
    for f in fileNames:
        if f.endswith('.xml'):
            file = os.path.join(dirName, f)
            tree = ET.parse(file)
            root = tree.getroot()
            if root.tag == '{http://www.isotc211.org/2005/gmd}MD_Metadata':
                print (f)
                citation = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation', namespaces=namespaces)
                title = root.find(citeinfo + 'gmd:title/gco:CharacterString', namespaces=namespaces)
                date = root.find(citeinfo + 'gmd:date/gmd:CI_Date/gmd:date/gco:Date', namespaces=namespaces)
                URL = root.find(citeinfo + 'gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString', namespaces=namespaces)
                edition = root.find(citeinfo + 'gmd:edition', namespaces=namespaces)
                credit = root.find(idinfo + 'gmd:credit/gco:CharacterString', namespaces=namespaces)
                metadataID = root.find('gmd:fileIdentifier/gco:CharacterString', namespaces=namespaces)
                URI = root.find('gmd:dataSetURI/gco:CharacterString', namespaces=namespaces)
                mdDateStamp = root.find('gmd:dateStamp/gco:DateTime', namespaces=namespaces)
                topicCategory = root.find(idinfo + 'gmd:topicCategory/gmd:MD_TopicCategoryCode', namespaces=namespaces)
                publisher = root.findall(citeinfo + 'gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString', namespaces=namespaces)
                md_keywords = root.findall(idinfo + 'gmd:descriptiveKeywords/gmd:MD_Keywords', namespaces=namespaces)
                all_keywords = root.findall(idinfo + 'gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword/gco:CharacterString', namespaces=namespaces)
                placeKeywords = root.findall(idinfo + 'gmd:descriptiveKeywords[1]/gmd:MD_Keywords[1]/gmd:keyword', namespaces=namespaces)
                md_placeKeywords = root.findall(idinfo + 'gmd:descriptiveKeywords[1]/gmd:MD_Keywords[1]', namespaces=namespaces)
                themeKeyword = root.find(idinfo + 'gmd:descriptiveKeywords[2]/gmd:MD_Keywords[1]/gmd:keyword/gco:CharacterString', namespaces=namespaces)
                themeKeywords = root.findall(idinfo + 'gmd:descriptiveKeywords[2]/gmd:MD_Keywords[1]/gmd:keyword', namespaces=namespaces)
                md_themeKeywords = root.findall(idinfo + 'gmd:descriptiveKeywords[2]/gmd:MD_Keywords[1]', namespaces=namespaces)
                placeKeyword = root.find(idinfo + 'gmd:descriptiveKeywords[1]/gmd:MD_Keywords[1]/gmd:keyword/gco:CharacterString', namespaces=namespaces)
                language = root.find(idinfo + 'gmd:language', namespaces=namespaces)
                collection = root.find(idinfo + 'gmd:aggregationInfo/gmd:MD_AggregateInformation/gmd:aggregateDataSetName/gmd:CI_Citation/gmd:title/gco:CharacterString', namespaces=namespaces)
                collectionID = root.find(idinfo + 'gmd:aggregationInfo/gmd:MD_AggregateInformation/gmd:aggregateDataSetName/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString', namespaces=namespaces)
                distFormat = root.find('gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString', namespaces=namespaces)
                distributor = root.find('gmd:distributionInfo/gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor/gmd:distributorContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString', namespaces=namespaces)
                abstract = root.find(idinfo + 'gmd:abstract/gco:CharacterString', namespaces=namespaces)
                distURL = root.find(distinfo + 'gmd:linkage/gmd:URL', namespaces=namespaces)
                distName = root.find(distinfo +'gmd:name/gco:CharacterString',namespaces=namespaces)
                tempInstant = root.find(idinfo + 'gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent/gml:TimeInstant/gml:timePosition', namespaces=namespaces)
                mdDateStamp = root.find("gmd:dateStamp/gco:DateTime", namespaces=namespaces)
                fcID = root.find('gmd:contentInfo/gmd:MD_FeatureCatalogueDescription/gmd:featureCatalogueCitation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString', namespaces=namespaces)
                rights = root.find('gmd:identificationInfo[1]/gmd:MD_DataIdentification[1]/gmd:resourceConstraints[1]/gmd:MD_LegalConstraints[1]/gmd:otherConstraints[1]/gco:CharacterString[1]', namespaces=namespaces)
                auth = root.find('gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString', namespaces=namespaces)
                code = root.find('gmd:referenceSystemInfo/gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString', namespaces=namespaces)
                west = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal', namespaces=namespaces)
                east = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal', namespaces=namespaces)
                south = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal', namespaces=namespaces)
                north = root.find('gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal', namespaces=namespaces)
                fSize = root.find('gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:transferSize/gco:Real', namespaces=namespaces)
                geomTypeCode = root.find('gmd:spatialRepresentationInfo/gmd:MD_VectorSpatialRepresentation/gmd:geometricObjects/gmd:MD_GeometricObjects/gmd:geometricObjectType/gmd:MD_GeometricObjectTypeCode', namespaces=namespaces)
                createMetadata()