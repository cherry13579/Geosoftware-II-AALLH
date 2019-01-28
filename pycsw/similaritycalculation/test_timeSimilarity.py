# author: Aysel Tandik
# Testing timeSimilarity
# 09.01.2018, 16.01.2018

import timeSimilarity
import unittest

# Testing the three methods individually


def test_timeLength():
    result1 = timeSimilarity.timeLength(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                        '2015/12/04 15:28:59.122000 GMT+0', '2015/12/04 15:28:59.122000 GMT+0', 0])
    assert result1 == 0
    # 50years and 100 years
    result2 = timeSimilarity.timeLength(['1950/01/01 00:00:00 GMT+0', '2001/01/01 00:00:00 GMT+0', 730.5], [
                                        '2000/01/01 00:00:00 GMT+0', '2101/01/01 00:00:00 GMT+0', 0])
    assert result2 == 0.5


def test_timeOverlap():
    result = timeSimilarity.timeOverlap(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                        '2015/12/04 15:28:59.122000 GMT+0', '2015/12/04 15:28:59.122000 GMT+0', 0])
    assert result == 0.54


def test_similarInterval():
    result = timeSimilarity.similarInterval(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                            '2015/12/04 15:28:59.122000 GMT+0', '2015/12/04 15:28:59.122000 GMT+0', 0])
    assert result == 0.0

# This test shows the 100 percent similarity from the function


def test_Similartime():
    result1 = timeSimilarity.timeLength(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                        '1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5])
    result2 = timeSimilarity.timeOverlap(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                         '1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5])
    result3 = timeSimilarity.similarInterval(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                             '1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5])
    assert result1 == 1
    assert result2 == 1
    assert result3 == 1

# In this test is nothing similar so we have to achieve the result 0 for "no similarity"


def test_NotSimilartime():
    result1 = timeSimilarity.timeLength(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                        '1914/01/01 00:00:00 GMT+0', '1914/01/01 00:00:00 GMT+0', 123])
    result2 = timeSimilarity.timeOverlap(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                         '2088/01/01 00:00:00 GMT+0', '2089/01/01 00:00:00 GMT+0', 123])
    result3 = timeSimilarity.similarInterval(['1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 730.5], [
                                             '1956/01/01 00:00:00 GMT+0', '2088/01/01 00:00:00 GMT+0', 0])
    # 50years and 100 years
    result4 = timeSimilarity.timeLength(['1950/01/01 00:00:00 GMT+0', '2001/01/01 00:00:00 GMT+0', 730.5], [
                                        '2000/01/01 00:00:00 GMT+0', '2101/01/01 00:00:00 GMT+0', 0])
    assert result1 == 0
    assert result2 == 0
    assert result3 == 0
