# Auhtor Aysel Tandik
# 17.01.2019

import unittest
import getTimeExtent

def test_getTime():
    #Netcdf, aus Testdaten getestet, frage ist sonst wie soll ich das selber irgendwo herbekommen? 
    result = getTimeExtent.getTimeExtent("tos_O1_2001-2002.nc", "C:\\Users\\celeb\\Desktop\\Testdaten\\NetCDF")
    assert result == (['2001/01/16', '2002/12/16', 30.391304347826086], None)

def test_getTime():
    #aktuell liest getTimeExtent kein Geojson und auch kein csv