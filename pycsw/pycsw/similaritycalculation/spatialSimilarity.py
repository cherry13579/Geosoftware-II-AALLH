from math import *

from osgeo import gdal, ogr, osr


def spatialOverlap(bboxA, bboxB):
    """Calculates how much two boundingboxes overlap eachother. If the bbox is a point, it gets a buffer of 500 meters.
    :bboxA first bbox
    :bboxB second bbox
    :return: value in [0,1] (percant of overlap)
    """
    # get Boundingboxes as Geometries in WGS84 Mercator
    boxA = _generateGeometryFromBbox(bboxA)
    boxB = _generateGeometryFromBbox(bboxB)

    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    # if bboxes are not a polygon, they get a radisu where spatial correlation is possible (500m raduis)
    if areaA == 0:
        bufferDist = 500
        boxA = boxA.Buffer(bufferDist)
        areaA = boxA.GetArea()

    if areaB == 0:
        bufferDist = 500
        boxB = boxB.Buffer(bufferDist)
        areaB = boxB.GetArea()

    largerArea = areaA if areaA >= areaB else areaB

    # get the intersection area of the two bboxes
    intersection = boxA.Intersection(boxB)
    intersectGeometry = ogr.CreateGeometryFromWkt(intersection.ExportToWkt())

    intersectArea = intersectGeometry.GetArea()

    # get percentage of overlap
    reachedPercentArea = intersectArea/largerArea
    return reachedPercentArea


def similarArea(bboxA, bboxB):
    """Calculates how similar the area of the two boundingboxes are.
    :bboxA first bbox
    :bboxB second bbox
    :return: value in [0,1] (percant of similar area)
    """
    # get Boundingboxes as Geometries in WGS84 Mercator
    boxA = _generateGeometryFromBbox(bboxA)
    boxB = _generateGeometryFromBbox(bboxB)

    # get box area
    areaA = boxA.GetArea()
    areaB = boxB.GetArea()

    reachedPercentArea = 0

    # get percentage of equal area size
    if areaA == areaB:
        reachedPercentArea = 1
    else:
        if areaA >= areaB:
            reachedPercentArea = areaB/areaA
        else:
            reachedPercentArea = areaA/areaB

    return reachedPercentArea


def spatialDistance(bboxA, bboxB):
    """Calculates how close two boundingboxes are to each other, depending on the diagonal diameter of the larger boundingbox
    :bboxA first bbox
    :bboxB second bbox
    :return: value in [0,1] (percant of distance)
    """
    distBetweenCenterPoints = None
    longerDistance = None
    # if both bboxes are points, they get a maximum distance of 5km (>5km means no spacial relation)
    if (bboxA[0] == bboxA[2]) and (bboxB[0] == bboxB[2]) and (bboxA[1] == bboxA[3]) and (bboxB[1] == bboxB[3]):
        distBetweenCenterPoints = _getDistance(
            (bboxA[0], bboxA[1]), (bboxB[0], bboxB[1]))
        longerDistance = 5

    else:
        # check if bboxA is a point
        if (bboxA[0] == bboxA[2]) and (bboxA[1] == bboxA[3]):
            centerA = ogr.CreateGeometryFromWkt(
                "POINT (%f %f)" % (bboxA[0], bboxA[1]))
        # if not, the centerpooint of the bbox will be calculated
        else:
            centerA = _getMidPoint(bboxA)

        if (bboxB[0] == bboxB[2]) and (bboxB[1] == bboxB[3]):
            centerB = ogr.CreateGeometryFromWkt(
                "POINT (%f %f)" % (bboxB[0], bboxB[1]))
        else:
            centerB = _getMidPoint(bboxB)

        # calculate the diagonal diameter of the bboxes and take the longer distance
            # as a reference for spatial correlation
        distA = _getDistance((bboxA[1], bboxA[0]), (bboxA[3], bboxA[2]))
        distB = _getDistance((bboxB[1], bboxB[0]), (bboxB[3], bboxB[2]))

        longerDistance = distA if distA >= distB else distB

        distBetweenCenterPoints = _getDistance(
            (centerA.GetY(), centerA.GetX()), (centerB.GetY(), centerB.GetX()))

    # calculate the linear falling distance between the centerpoints
    if distBetweenCenterPoints is not None and longerDistance is not None:
        distPercentage = (1 - (distBetweenCenterPoints/longerDistance))
        return distPercentage if distPercentage > 0 else 0
    else:
        print("Error while processing")
        return 0


#############################################################################


def _generateGeometryFromBbox(bbox):
    """private function! returns an ogr-Geometry for a boundingbox
    :param bbox boundingbox to be converted
    :returns: bbox as ogr-geometry in WGS84 Mercator Projection
    """
    gdal.UseExceptions()
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(25832)

    boxA = ogr.CreateGeometryFromGML("""
    <gml:Polygon xmlns:gml="http://www.opengis.net/gml" srsName="http://www.opengis.net/def/crs/EPSG/0/25832">
        <gml:outerBoundaryIs>
            <gml:LinearRing>
                <gml:coordinates>
                    %(minX)f,%(minY)f %(minX)f,%(maxY)f %(maxX)f,%(maxY)f %(maxX)f,%(minY)f %(minX)f,%(minY)f
                </gml:coordinates>
            </gml:LinearRing>
        </gml:outerBoundaryIs>
    </gml:Polygon>
    """ % ({'minX': bbox[0], 'minY': bbox[1], 'maxX': bbox[2], 'maxY': bbox[3]}))

    transform = osr.CoordinateTransformation(source, target)
    boxA.Transform(transform)
    # print(boxA.GetSpatialReference().ExportToPrettyWkt())
    return boxA


def _getDistance(startingpoint, endpoint):
    """calculates the distance between tow wgs84 coordinates
    :param startingpoint in WGS84 - startingpoint[lat, lon]
    :param endpoint in WGS84 - endpoint[lat, lon]
    :see http://www.movable-type.co.uk/scripts/latlong.html
    :returns: distance between the points in km
    """
    radius = 6371
    radLat1 = (startingpoint[0] * pi) / 180
    radLat2 = (endpoint[0] * pi) / 180
    deltLat = ((endpoint[0] - startingpoint[0]) * pi) / 180
    deltLon = ((endpoint[1] - startingpoint[1]) * pi) / 180

    a = sin(deltLat / 2) * sin(deltLat / 2) + cos(radLat1) * \
        cos(radLat2) * sin(deltLon / 2) * sin(deltLon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c
    return d


def _getMidPoint(bbox):
    line1 = "LINESTRING (%f %f, %f %f)" % (bbox[0], bbox[1], bbox[2], bbox[3])
    line2 = "LINESTRING (%f %f, %f %f)" % (bbox[2], bbox[1], bbox[0], bbox[3])

    line1 = ogr.CreateGeometryFromWkt(line1)
    line2 = ogr.CreateGeometryFromWkt(line2)

    intersectionPoint = line1.Intersection(line2)
    intersectGeometry = ogr.CreateGeometryFromWkt(
        intersectionPoint.ExportToWkt())

    datatype = intersectGeometry.GetGeometryName()

    if str.upper(datatype) == "LINESTRING":
        if bbox[1] == bbox[3]:
            line1 = "LINESTRING (%f %f, %f %f)" % (
                bbox[0], bbox[1]-0.001, bbox[2], bbox[3]+0.001)
            line2 = "LINESTRING (%f %f, %f %f)" % (
                bbox[2], bbox[1]-0.001, bbox[0], bbox[3]+0.001)

        elif bbox[0] == bbox[2]:
            line1 = "LINESTRING (%f %f, %f %f)" % (
                bbox[0]-0.001, bbox[1], bbox[2]+0.001, bbox[3])
            line2 = "LINESTRING (%f %f, %f %f)" % (
                bbox[2]-0.001, bbox[1], bbox[0]+0.001, bbox[3])

        line1 = ogr.CreateGeometryFromWkt(line1)
        line2 = ogr.CreateGeometryFromWkt(line2)

        intersectionPoint = line1.Intersection(line2)
        intersectGeometry = ogr.CreateGeometryFromWkt(
            intersectionPoint.ExportToWkt())

    return intersectGeometry


###############################################################################

# print(_getDistance((0,0), (0,1)))
# Geometry
# print("\n Geometry \n")
# bbox1 = [13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134]
# bbox2 = [17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# Points
# print("\n Points \n")
# bbox1 = [13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435]
# bbox2 = [13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435]
# print(spatialDistance(bbox1, bbox2))
# print(spatialOverlap(bbox1, bbox2))
# print(similarArea(bbox1, bbox2))

# wkt = "LINESTRING(0 0,0.0 1)"
# geom = ogr.CreateGeometryFromWkt(wkt)
# source = osr.SpatialReference()
# source.ImportFromEPSG(4326)

# target = osr.SpatialReference()
# target.ImportFromEPSG(25832)

# transform = osr.CoordinateTransformation(source, target)
# geom.Transform(transform)
# print(geom.ExportToWkt())
# print(geom.GetSpatialReference().ExportToWkt)
# print(geom.Length())

# gml = """<gml:Point xmlns:gml="http://www.opengis.net/gml"><gml:coordinates>108420.33,753808.59</gml:coordinates></gml:Point>"""
# point = ogr.CreateGeometryFromGML(gml)
# print("%d,%d" % (point.GetX(), point.GetY()))

# wkt = "POINT (1198054.34 648493.09)"
# pt = ogr.CreateGeometryFromWkt(wkt)
# bufferDistance = 500
# poly = pt.Buffer(bufferDistance)
# print ("%s buffered by %d is %s" % (pt.ExportToWkt(), bufferDistance, poly.ExportToWkt()))

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
