# Author Aysel Tandik
# 16.01.2019

import unittest
import getBoundingBox

def test_getBBJson():
    # Dijon (nähe Paris)
    result = getBoundingBox.getBoundingBox("testBBJson.geojson", "C:\\Users\\celeb\\Desktop\\Testdaten\\GeoJSON")
    assert result == ([3.5218322277,46.7697482029, 7.4549376965,48.574577168], None)
#def test_getBBCsv():
    # um Münster herum
    #http://bboxfinder.com/#51.041394,8.085938,52.762892,10.942383
    # 5.1468,46.5123,7.8335,48.1635

def test_getBBLine():
    result = getBoundingBox.getBoundingBox("lineString.geojson", "C:\\Users\\celeb\\Desktop\\Testdaten\\GeoJSON")
    assert result == ([6.564331, 51.108696, 7.099915, 51.280817], None)
