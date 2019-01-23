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