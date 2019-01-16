from osgeo import ogr

wkt1 = "POLYGON ((1 1, 1 1, 1 1, 1 1, 1 1))"
wkt2 = "POLYGON ((0 0, 0 0, 0 0, 0 0, 0 0)))"

poly1 = ogr.CreateGeometryFromWkt(wkt1)
poly2 = ogr.CreateGeometryFromWkt(wkt2)

intersection = poly1.Intersection(poly2)

if intersection.ExportToWkt() == "GEOMETRYCOLLECTION EMPTY":
    print(True)
print(intersection)
print (intersection.ExportToWkt())