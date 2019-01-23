from math import *
from osgeo import gdal, ogr, osr
import logging 

LOGGER = logging.getLogger(__name__)

#LOGGER.info('Spatial similarity is calculated.')

def spatialOverlap(bboxA, bboxB):

    return 0.1

    wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
    wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"

    poly1 = ogr.CreateGeometryFromWkt(wkt1)
    poly2 = ogr.CreateGeometryFromWkt(wkt2)

    print(poly1, poly2)
    union = poly1.Union(poly2)
    intersection = poly1.Intersection(poly2)
    print(union, intersection)
    print ("WICHTIG "+ union.ExportToWkt())

    print(bboxA, bboxB)
    # get Boundingboxes as Geometries
    boxA = _generateGeometryFromBbox(bboxA)
    boxB = _generateGeometryFromBbox(bboxB)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    print(areaA, areaB)

    if (areaA == 0) and (areaB == 0):
        bufferDist = 328 # foot = 500 Meter
        boxA = boxA.Buffer(bufferDist)
        boxB = boxB.Buffer(bufferDist)

        areaA = boxA.GetArea()
        areaB = boxB.GetArea()

    # print(areaA)

    largerArea = areaA if areaA >= areaB else areaB
    
    print(boxA, boxB)
    intersection = boxA.Intersection(boxB)
    print(intersection)
    intersectGeometry = ogr.CreateGeometryFromWkt(intersection.ExportToWkt())

    intersectArea = intersectGeometry.GetArea()

    # print(intersectArea)

    reachedPercentArea = intersectArea*100/largerArea

    reachedPercentArea = floor(reachedPercentArea * 100)/100
    # print(reachedPercentArea)
    ##LOGGER.info('Result spatial Overlap: '+ reachedPercentArea +'.')
    return reachedPercentArea


def similarArea(bboxA, bboxB):

    boxA = _generateGeometryFromBbox(bboxA)
    boxB = _generateGeometryFromBbox(bboxB)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    reachedPercentArea = 0

    if areaA == areaB:
        reachedPercentArea = 100
    else:
        if areaA >= areaB:
            reachedPercentArea = areaB/areaA
        else:
            reachedPercentArea = areaA/areaB

    #LOGGER.info('Result similar Area: '+ reachedPercentArea +'.')
    return reachedPercentArea


def spatialDistance(bboxA, bboxB):

    return 0.1

    distBetweenCenterPoints = None
    longerDistance = None
    if (bboxA[0] == bboxA[2]) and (bboxB[0] == bboxB[2]) and (bboxA[1] == bboxA[3]) and (bboxB[1] == bboxB[3]):
        distBetweenCenterPoints = _getDistance((bboxA[0], bboxA[1]), (bboxB[0], bboxB[1]))
        longerDistance = 5

    else:
        if (bboxA[0] == bboxA[2]) and (bboxA[1] == bboxA[3]):
            centerA = ogr.CreateGeometryFromWkt("POINT (%f %f)" % (bboxA[0], bboxA[1]))
        else:
            centerA = _getMidPoint(bboxA)

        if (bboxB[0] == bboxB[2]) and (bboxB[1] == bboxB[3]):
            centerB = ogr.CreateGeometryFromWkt("POINT (%f %f)" % (bboxB[0], bboxB[1]))
        else:
            centerB = _getMidPoint(bboxB)

        type1 = centerA.GetGeometryName()
        type2 = centerB.GetGeometryName()
        # print(type1, type2)

        distA = _getDistance((bboxA[1], bboxA[0]), (bboxA[3], bboxA[2]))
        distB = _getDistance((bboxB[1], bboxB[0]), (bboxB[3], bboxB[2]))

        # print(distA, distB)

        longerDistance = distA if distA >= distB else distB

        # print(longerDistance)

        distBetweenCenterPoints = _getDistance((centerA.GetY(), centerA.GetX()),(centerB.GetY(), centerB.GetX()))
        # print(distBetweenCenterPoints)

    if distBetweenCenterPoints is not None and longerDistance is not None:
        distPercentage = (1 - (distBetweenCenterPoints/longerDistance)) * 100
        distPercentage = floor(distPercentage * 100)/100
        # print(distPercentage if distPercentage>0 else 0)
        #LOGGER.info('Result spatial distance: '+ distPercentage +'.')
        return distPercentage if distPercentage>0 else 0
    else:
        #LOGGER.error('Error while processing.')
        return 0


# def sameDatasetType(file1, file2):
#     file1isRaster = None
#     file2isRaster = None
#     try:
#         gdal.UseExceptions()
#         gdal.Open(file1)
#         file1isRaster = True

#         gdal.Open(file2)
#         file2isRaster = True
#     except:
#         try:
#             ogr.UseExceptions()
#             args = ['ogrinfo', '-ro', '-so', '-al', '%s' % file1]
#             process = Popen(args, stdout=PIPE, stderr=PIPE)
#             file1isRaster = False
#             args = ['ogrinfo', '-ro', '-so', '-al', '%s' % file2]
#             process = Popen(args, stdout=PIPE, stderr=PIPE)
#             file2isRaster = False
#         except:
#             return 0
#         else:
#             return 100
#     else:
#         return 100


#############################################################################


def _generateGeometryFromBbox(bbox):
    # print(bbox)

    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    target = osr.SpatialReference()
    target.ImportFromEPSG(2927)

    boxA = ogr.CreateGeometryFromJson("""{
            "type":"Polygon",
            "coordinates":[
                [
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ],
                    [
                        %f,%f
                    ]
                ]
            ]
        }""" % (bbox[0],bbox[1], bbox[0], bbox[3], bbox[2], bbox[3], bbox[2], bbox[1], bbox[0], bbox[1]))

    
    transform = osr.CoordinateTransformation(source, target)
    # boxA.Transform(transform)

    return boxA

def _getDistance(startingpoint, endpoint):
    """
    input: in WGS84 - startingpoint[lat, lon], endpoint[lat, lon]
    @see http://www.movable-type.co.uk/scripts/latlong.html
    """
    radius = 6371
    radLat1 = (startingpoint[0] * pi) / 180
    radLat2 = (endpoint[0] * pi) / 180
    deltLat = ((endpoint[0] - startingpoint[0]) * pi ) / 180
    deltLon = ((endpoint[1] - startingpoint[1]) * pi ) / 180

    a = sin(deltLat / 2) * sin(deltLat / 2) + cos(radLat1) * cos(radLat2) * sin(deltLon / 2) * sin(deltLon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c
    return d

def _getMidPoint(bbox):
    print(bbox)
    line1 = "LINESTRING (%f %f, %f %f)" % (bbox[0], bbox[1], bbox[2], bbox[3])
    line2 = "LINESTRING (%f %f, %f %f)" % (bbox[2], bbox[1], bbox[0], bbox[3])
    print(line1, line2)
    line1 = ogr.CreateGeometryFromWkt(line1)
    line2 = ogr.CreateGeometryFromWkt(line2)

    intersectionPoint = line1.Intersection(line2)
    # z = intersectionPoint.ExportToWkt()
    intersectGeometry = ogr.CreateGeometryFromWkt(intersectionPoint.ExportToWkt())

    datatype = intersectGeometry.GetGeometryName()

    if str.upper(datatype) == "LINESTRING":
        if bbox[1] == bbox[3]:
            line1 = "LINESTRING (%f %f, %f %f)" % (bbox[0], bbox[1]-0.001, bbox[2], bbox[3]+0.001)
            line2 = "LINESTRING (%f %f, %f %f)" % (bbox[2], bbox[1]-0.001, bbox[0], bbox[3]+0.001)

        elif bbox[0] == bbox[2]:
            line1 = "LINESTRING (%f %f, %f %f)" % (bbox[0]-0.001, bbox[1], bbox[2]+0.001, bbox[3])
            line2 = "LINESTRING (%f %f, %f %f)" % (bbox[2]-0.001, bbox[1], bbox[0]+0.001, bbox[3])

        line1 = ogr.CreateGeometryFromWkt(line1)
        line2 = ogr.CreateGeometryFromWkt(line2)

        intersectionPoint = line1.Intersection(line2)
        intersectGeometry = ogr.CreateGeometryFromWkt(intersectionPoint.ExportToWkt())

        datatype2 = intersectGeometry.GetGeometryName()


    return intersectGeometry


###############################################################################       

# 124.99553571 67.99553636, 124.99553571 72.00446429, 165.00445788 72.00446429, 165.00445788 67.99553636, 124.99553571 67.99553636

# Geometry
# print("\n Geometry \n")
# bbox1 = [13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134]
# bbox2 = [124.99553571, 67.99553636, 165.00445788, 72.00446429]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# # Points
# print("\n Points \n")
# bbox1 = [13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435]
# bbox2 = [13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))


# # Line and Point
# print("\n Line and Point \n")
# bbox1 = [11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435]
# bbox2 = [13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# # Polygon and Point
# print("\n Polygon and Point \n")
# bbox1 = [13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134]
# bbox2 = [13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# # Same BoundingBox
# print("\n Same BoundingBox \n")
# bbox1 = [0.439453,29.688053,3.911133,31.765537]
# bbox2 = [0.439453,29.688053,3.911133,31.765537]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# # Ähnliche BoundingBox, die nah beieinander liegt
# print("\n Similar Bounding Box which are close to each other \n")
# bbox1 = [7.596703,51.950402,7.656441,51.978536]
# bbox2 = [7.588205,51.952412,7.616014,51.967644]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# # Weit entfernte Boundingboxen 
# print("\n Not so related Bounding Box \n")
# bbox1 = [7.596703,51.950402,7.656441,51.978536]
# bbox2 = [-96.800194,32.760085,-96.796353,32.761385]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))