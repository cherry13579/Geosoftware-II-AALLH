# Author: Lia Kirsch

import spatialSimilarity
import math

# Geometry
def test_spatialdistance_Geometry():
    total = spatialSimilarity.spatialDistance([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134], [
                                              17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686])
    assert  math.floor(total * 100)/100 == 0.74


def test_spatialOverlap_Geometry():
    total = spatialSimilarity.spatialOverlap([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134], [
                                             17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686])
    assert math.floor(total * 100)/100 == 0.41


def test_similarArea_Geometry():
    total = spatialSimilarity.similarArea([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134], [
                                          17.7978515625, 52.09300763963822, 7.27294921875, 46.14939437647686])
    assert math.floor(total * 100)/100 == 0.58

# Points
def test_spatialdistance_Points():
    total = spatialSimilarity.spatialDistance([13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435], [
                                              13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.99


def test_spatialOverlap_Points():
    total = spatialSimilarity.spatialOverlap([13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435], [
                                             13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.96


def test_similarArea_Points():
    total = spatialSimilarity.similarArea([13.0078125, 50.62507306341435, 13.0078125, 50.62507306341435], [
                                          13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 1.0

##Line and Point
def test_spatialdistance_LineAndPoint():
    total = spatialSimilarity.spatialDistance([11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435], [
                                              13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.49


def test_spatialOverlap_LineAndPoint():
    total = spatialSimilarity.spatialOverlap([11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435], [
                                             13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 10000)/10000 == 0.0002


def test_similarArea_LineAndPoint():
    total = spatialSimilarity.similarArea([11.0078125, 50.62507306341435, 13.0078125, 50.62507306341435], [
                                          13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.0

## Polygon and Point
def test_spatialdistance_PolygonAndPoint():
    total = spatialSimilarity.spatialDistance([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134], [
                                              13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.5


def test_spatialOverlap_PolygonAndPoint():
    total = spatialSimilarity.spatialOverlap([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134], [
                                             13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.0


def test_similarArea_PolygonAndPoint():
    total = spatialSimilarity.similarArea([13.0078125, 50.62507306341435, 5.44921875, 45.82879925192134], [
                                          13.0082125, 50.62513301341435, 13.0082125, 50.62513301341435])
    assert math.floor(total * 100)/100 == 0.0

# SameBoundingBox
def test_spatialdistance_SameBoundingBox():
    total = spatialSimilarity.spatialDistance([0.439453, 29.688053, 3.911133, 31.765537], [
                                              0.439453, 29.688053, 3.911133, 31.765537])
    assert math.floor(total * 100)/100 == 1.00


def test_spatialOverlap_SameBoundingBox():
    total = spatialSimilarity.spatialOverlap([0.439453, 29.688053, 3.911133, 31.765537], [
                                             0.439453, 29.688053, 3.911133, 31.765537])
    assert math.floor(total * 100)/100 == 1.0


def test_similarArea_SameBoundingBox():
    total = spatialSimilarity.similarArea([0.439453, 29.688053, 3.911133, 31.765537], [
                                          0.439453, 29.688053, 3.911133, 31.765537])
    assert math.floor(total * 100)/100 == 1.0

# similar boundingBoxes that are close together
def test_spatialdistance_SBBTACT():
    total = spatialSimilarity.spatialDistance([7.596703, 51.950402, 7.656441, 51.978536], [
                                              7.588205, 51.952412, 7.616014, 51.967644])
    assert math.floor(total * 100)/100 == 0.66


def test_spatialOverlap_SSBBTACT():
    total = spatialSimilarity.spatialOverlap([7.596703, 51.950402, 7.656441, 51.978536], [
                                             7.588205, 51.952412, 7.616014, 51.967644])
    assert math.floor(total * 100)/100 == 0.17


def test_similarArea_SBBTACT():
    total = spatialSimilarity.similarArea([7.596703, 51.950402, 7.656441, 51.978536], [
                                          7.588205, 51.952412, 7.616014, 51.967644])
    assert math.floor(total * 100)/100 == 0.25


# Far away boundingboxes
def test_spatialdistance_fABB():
    total = spatialSimilarity.spatialDistance(
        [7.596703, 51.950402, 7.656441, 51.978536], [-96.800194, 32.760085, -96.796353, 32.761385])
    assert math.floor(total * 100)/100 == 0


def test_spatialOverlap_fABB():
    total = spatialSimilarity.spatialOverlap(
        [7.596703, 51.950402, 7.656441, 51.978536], [-96.800194, 32.760085, -96.796353, 32.761385])
    assert math.floor(total * 100)/100 == 0.0


def test_similarArea_fABB():
    total = spatialSimilarity.similarArea(
        [7.596703, 51.950402, 7.656441, 51.978536], [-96.800194, 32.760085, -96.796353, 32.761385])

    assert math.floor(total * 10000)/10000 == 0.0032
