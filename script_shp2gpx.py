from osgeo import ogr, osr

##InputFile=vector
##Field_Name=field InputFile
##Field_Desc=field InputFile
##outputFile=output file

Field_Name = str(Field_Name) 
Field_Desc = str(Field_Desc)


def writeNameAndDesc(feature):
    name = feature.GetField(Field_Name)
    if type(name) is not unicode:
        name = unicode(name)
    nameTag = u'<name>'+name+'</name>'
    outputGPX.write(nameTag.encode('utf-8'))
    if Field_Desc != "":
        desc = feature.GetField(Field_Desc)
        if type(desc) is not 'unicode':
            desc = unicode(desc)
        descTag = u'<desc>'+desc+'</desc>'
        outputGPX.write(descTag.encode('utf-8'))

def writePoint(feature):
    geom = feature.GetGeometryRef()
    geom.Transform(coordTransform)
    xCoord = str(geom.GetX())
    yCoord = str(geom.GetX())
    coord= '<wpt lat="'+yCoord+'" lon="'+xCoord+'">'
    outputGPX.write(coord.encode('utf-8'))
    writeNameAndDesc(feature)
    outputGPX.write('</wpt> \n')


def writePolyLine(feature):
        outputGPX.write("<trk>")
        writeNameAndDesc(feature)
        outputGPX.write("<trkseg> \n")

        geom =  feature.GetGeometryRef()
        geom.Transform(coordTransform)
        for i in range(0, geom.GetPointCount()):
            point = geom.GetPoint(i)
            xCoord = str(point[0])
            yCoord = str(point[1])
            coordWrite = '<trkpt lat="'+yCoord+'" lon="'+xCoord+'"> </trkpt> \n '
            outputGPX.write(coordWrite.encode('utf-8'))
        outputGPX.write('</trkseg></trk> \n ')




outputGPX = open(outputFile, 'w')

header = """<?xml version="1.0" encoding="UTF-8"?> <gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\
<metadata>
<time>?</time>
</metadata> \n'"""
strHeader = header.encode('utf-8')
outputGPX.write(strHeader)


DriverName = "ESRI Shapefile"
driver = ogr.GetDriverByName(DriverName)
dataSource = driver.Open(InputFile)
layer = dataSource.GetLayer()



#projection stuff
inSpatialRef = layer.GetSpatialRef()
outSpatialRef = osr.SpatialReference() 
outSpatialRef.ImportFromEPSG(4326)
coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)


#output GPX

layerType = layer.GetGeomType()
#1 = point, 2 = polyligne


for feature in layer:
    if layerType == 1:
        writePoint(feature)
    if layerType == 2:
        writePolyLine(feature)

outputGPX.write('</gpx>')
outputGPX.close()
