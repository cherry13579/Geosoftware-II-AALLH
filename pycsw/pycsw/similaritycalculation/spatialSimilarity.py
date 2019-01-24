from math import *

# add local modules folder
# file_path = os.path.join('..', 'Python_Modules')
# sys.path.append(file_path)

from osgeo import gdal, ogr, osr
# from subprocess import Popen, PIPE

def spatialOverlap(bboxA, bboxB):
    # get Boundingboxes as Geometries
    print(bboxA, bboxB)
    boxA = _generateGeometryFromBbox(bboxA)
    boxB = _generateGeometryFromBbox(bboxB)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    if areaA == 0:
        bufferDist = 500
        boxA = boxA.Buffer(bufferDist)
        areaA = boxA.GetArea()
    
    if areaB == 0:
        bufferDist = 500
        boxB = boxB.Buffer(bufferDist)
        areaB = boxB.GetArea() 


    largerArea = areaA if areaA >= areaB else areaB

    intersection = boxA.Intersection(boxB)
    intersectGeometry = ogr.CreateGeometryFromWkt(intersection.ExportToWkt())

    intersectArea = intersectGeometry.GetArea()

    # print(intersectArea)

    reachedPercentArea = intersectArea/largerArea

    reachedPercentArea = floor(reachedPercentArea * 100)/100
    # print(reachedPercentArea)
    return reachedPercentArea


def similarArea(bboxA, bboxB):
    boxA = _generateGeometryFromBbox(bboxA)
    boxB = _generateGeometryFromBbox(bboxB)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    reachedPercentArea = 0

    if areaA == areaB:
        reachedPercentArea = 1
    else:
        if areaA >= areaB:
            reachedPercentArea = areaB/areaA
        else:
            reachedPercentArea = areaA/areaB

    reachedPercentArea = floor(reachedPercentArea*100)/100
    return reachedPercentArea


def spatialDistance(bboxA, bboxB):
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
        distPercentage = (1 - (distBetweenCenterPoints/longerDistance))
        distPercentage = floor(distPercentage * 100)/100
        # print(distPercentage if distPercentage>0 else 0)
        return distPercentage if distPercentage>0 else 0
    else:
        print("Error while processing")
        return 0


#############################################################################


def _generateGeometryFromBbox(bbox):
    gdal.UseExceptions()
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(25832)

    boxA = ogr.CreateGeometryFromJson("""{
            "type":"Polygon",
            "coordinates":[
                [
                    [
                        %(minX)f,%(minY)f
                    ],
                    [
                        %(minX)f,%(maxY)f
                    ],
                    [
                        %(maxX)f,%(maxY)f
                    ],
                    [
                        %(maxX)f,%(minY)f
                    ],
                    [
                        %(minX)f,%(minY)f
                    ]
                ]
            ]
        }""" % ({'minX':bbox[0], 'minY':bbox[1], 'maxX':bbox[2], 'maxY':bbox[3]}))

    # print(target.ExportToPrettyWkt())
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
    line1 = "LINESTRING (%f %f, %f %f)" % (bbox[0], bbox[1], bbox[2], bbox[3])
    line2 = "LINESTRING (%f %f, %f %f)" % (bbox[2], bbox[1], bbox[0], bbox[3])

    line1 = ogr.CreateGeometryFromWkt(line1)
    line2 = ogr.CreateGeometryFromWkt(line2)

    intersectionPoint = line1.Intersection(line2)
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

    return intersectGeometry


###############################################################################       


# # Geometry
# print("\n Geometry \n")
# bbox1 = [13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134]
# bbox2 = [17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686]
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
# bbox1 = [10.0078125, 50.62507306341435, 13.0078125, 50.62507306341435]
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
# bbox1 = [124.99553571, 67.99553636, 165.00445788, 72.00446429]
# bbox2 = [124.99553571, 67.99553636, 165.00445788, 72.00446429]
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

# Geometry

# 0.74
# 0.41
# 0.58

#  Points

# 0.99
# 0.81
# 1.0

#  Line and Point

# 0.49
# 0.0
# 1.0

#  Polygon and Point

# 0.5
# 0.0
# 0.0

#  Same BoundingBox

# 1.0
# 1.0
# 1.0

#  Similar Bounding Box which are close to each other

# 0.66
# 0.17
# 0.25

#  Not so related Bounding Box

# 0
# 0.0
# 0.0

# Geometry

# 0.74
# 0.41
# 0.57

#  Points

# 0.99
# 0.99
# 1.0

#  Line and Point

# 0.49
# 0.99
# 1.0

#  Polygon and Point

# 0.5
# 0.0
# 0.0

#  Same BoundingBox

# 1.0
# 1.0
# 1.0

#  Similar Bounding Box which are close to each other

# 0.66
# 0.17
# 0.25

#  Not so related Bounding Box

# 0
# 0.0
# 0.0