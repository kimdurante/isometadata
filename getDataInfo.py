from osgeo import gdal, osr, ogr
import os
import csv

#Create a csv of filenames and spatial reference systems (SRS), and data types.

output_file = open( 'layers.csv', 'w' )
headers = ['filename', 'spatial reference','type', 'west', 'south','east','north', 'format', 'identifier','title','description','originator','publisher','dateIssued','temporal','subject','topicCat','spatialSubject', 'fc_uuid','language', 'collectionTitle','collectionId','access','rights']
writer = csv.writer(output_file)
writer.writerow(headers)

#Find shapefiles in a directory. Open the data and get the SRS, geometry type, and extent.

for dirName, subDirs, fileNames in os.walk('.'):
    for f in fileNames:
        if f.endswith('.shp'):
            #print ('Filename: ' + f)
            filePath = os.path.join(dirName, f)
            ds = ogr.Open(filePath)
            for lyr in ds:
                srs = lyr.GetSpatialRef()
                try:
                   srs
                   srsAuth = srs.GetAttrValue('AUTHORITY',0)
                   srsCode = srs.GetAttrValue('AUTHORITY',1)
                   #print (f)
                except:
                    srsAuth = 'NONE'
                    srsCode = 'NONE' 
                    print ('Missing Spatial Reference ' + f)
                geomType = ogr.GeometryTypeToName(lyr.GetGeomType())
                (minx, maxx, miny, maxy) = lyr.GetExtent()
                #print ('Extent: %f, %f - %f %f' % (minx, miny, maxx, maxy)) #W-S-E-N
                west, south, east, north = minx, miny, maxx, maxy
                print (f)
            output_file.write(f + ',' + srsCode + ',' + geomType + ',' + str(minx) + ',' + str(miny) + ',' + str(maxx) + ',' + str(maxy) + ',' + 'Shapefile' + '\n')

 #Find geotiffs get SRS  and extent          
        else:
            if f.endswith('.tif'):     
                f = os.path.join(dirName, f)
                ds = gdal.Open(f)
                prj = ds.GetProjection()
                srs=osr.SpatialReference(wkt=prj)
                
                try:
                    srs
                    if srs.IsProjected:
                        #print (f)
                        srs = srs.GetAttrValue('authority', 0) + '::' + srs.GetAttrValue('authority', 1)
                        srsAuth =srs[4:]
                        srsCode =srs[6:]
                except:
                    srsAuth = 'NONE'
                    srsCode = 'NONE'
                    print ('Missing spatial reference ' +f)
                gt = ds.GetGeoTransform()
                width = ds.RasterXSize
                height = ds.RasterYSize
                minx = gt[0]
                miny = gt[3] + width*gt[4] + height*gt[5]
                maxx = gt[0] + width*gt[1] + height*gt[2]
                maxy = gt[3]
                print (f)
                output_file.write(f + ',' + srsCode + ',' + 'Raster' + ',' + str(minx) + ','  + str(miny) + ',' + str(maxx) + ',' + str(maxy) + ',' + 'Raster' '\n')            

output_file.close()              
