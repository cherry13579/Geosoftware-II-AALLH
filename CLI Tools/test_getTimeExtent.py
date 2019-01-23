'''
Created on 17.01.2019
@author: Aysel Tandik
'''
import os
import sys
import tempfile
import unittest
import getTimeExtent

# add local modules folder
file_path = os.path.join('..', 'Testdata')
sys.path.append(file_path)

def test_getTimeNetCdf():
    timeextent = getTimeExtent.getTimeExtent("tos_O1_2001-2002.nc", file_path)
    assert timeextent == (['2001/01/16', '2002/12/16', 30.391304347826086], None)

def test_getTimeCsv():
    timeextent = getTimeExtent.getTimeExtent("kalterherberg_zeitreihe.csv", file_path)
    assert timeextent == (['2018/11/15', '2018/12/08', 1.0], None)

# Testing with only point in time, no time extent
def test_getTimeGeojson():
    pointInTime = getTimeExtent.getTimeExtent("muenster_ring_zeit.geojson", file_path)
    assert pointInTime == (['2018/12/17', '2018/12/17', 0], None)

# Testing the situation, where the datatype is not supported
def test_ErrorFile():
    errorfile = getTimeExtent.getTimeExtent("error.file", file_path)
    assert errorfile == (None, 'Filetype .file not yet supported')

# Testing where input at "date" is not a valid datetime
def test_FalseInputFile():
    falseInput = getTimeExtent.getTimeExtent("falsetime.geojson", file_path)
    assert falseInput == (None, 'File Error!')