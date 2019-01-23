'''
Created on 17.01.2019
@author: Aysel Tandik
'''

import os
import sys
import tempfile
import unittest
import getPolygon

# add local modules folder
file_path = os.path.join('..', 'Testdata')
sys.path.append(file_path)

def test_Geojson():
    # Data with Polygon and Point
    result = getPolygon.getPolygon("getPolygonData.geojson", file_path)
    assert result == ([(3.5595703125, 46.558860303117164), (13.9306640625, 46.558860303117164), (13.9306640625, 51.23440735163459), (3.5595703125, 51.23440735163459)], None)

def test_LineGeojson():
    result = getPolygon.getPolygon("lineString.geojson", file_path)
    assert result == ([(6.564331, 51.119041), (7.099915, 51.108696), (6.995544, 51.280817)], None)

def test_ShapeFile():
    result = getPolygon.getPolygon("POLYGON.shp", file_path)
    assert result == ([(51.94246595679555, 7.5951576232910165), (51.94341833637654, 7.594213485717774), (51.95341710118838, 7.606229782104492), (51.95727846118796, 7.613525390624999), (51.95648505819626, 7.61824607849121), (51.94447651219544, 7.59953498840332)], None)

def test_NetCdf():
    result = getPolygon.getPolygon("ECMWF_ERA-40_subset.nc", file_path)
    assert result == ([(0.0, -90.0), (0.0, 90.0), (357.5, 90.0), (357.5, -90.0)], None)


# Testing the coordinate reference system from EPSG:3857 WGS 84 / Pseudo-Mercator
# to EPSG:4326 WGS 84 --> Result must be: lat: 9.96459, lon: 52.789476
def test_CRS():
    stringResult = getPolygon.CRSTransform(5876497.59, 1114888.69, 3857)
    string = str(stringResult[0])
    assert 0 == string.find("52.789476") # Longitude

    string2 = str(stringResult[1])
    assert 0 == string2.find("9.96459") # Latitude
