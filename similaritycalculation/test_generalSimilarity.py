# author: Lia Kirsch
# author2: Aysel Tandik (code improved and customized), 16.01.2019
# Testing generalSimilarity 
# 09.01.19

import generalSimilarity
import unittest


# Tests for the similar title method
def test_similarTitleTrue():
    total = generalSimilarity.similarTitle("1","1")
    assert total == 100

def test_similarTitleFalse():
    total = generalSimilarity.similarTitle("1","2")
    assert total == 0

def test_similarTitle50percent():
    total = generalSimilarity.similarTitle("abcd","abef")
    assert total == 50

def test_similarTitle25percent():
    total = generalSimilarity.similarTitle("abcd","aegf")
    assert total == 25

def test_similarTitle75percent():
    total = generalSimilarity.similarTitle("abcd","abcf")
    assert total == 75

# Test for the same Datatype
def test_sameDatatypeTRUE():
    total = generalSimilarity.sameDatatype(".txt", ".txt")
    assert total == 100

def test_sameDatatypeTRUE2():
    total = generalSimilarity.sameDatatype(".tif", ".geotif")
    assert total == 100

def test_sameDatatypeFalse():
    total = generalSimilarity.sameDatatype(".py", ".txt")
    assert total == 0

def test_sameDatatypeFalse2():
    total = generalSimilarity.sameDatatype(".js", ".txt")
    assert total == 0

def test_sameDatatypeFalse3():
    total = generalSimilarity.sameDatatype(".tiff", ".geotiifff")
    assert total == 0

def test_sameDatatypeFalse4():
    total = generalSimilarity.sameDatatype(".docs", ".txt")
    assert total == 0

# Test for the same Author
# author: Aysel Tandik
def test_sameAuthorTrue():
    result = generalSimilarity.sameAuthor("Max Mustermann", "Max Mustermann")
    assert result == 100

def test_notSameAuthor():
    result = generalSimilarity.sameAuthor("Alexander Müller", "Lisa Baum")
    assert result == 0

# Not the same auhtor even if one part from the last name contains in the second author
def test_sameAuthorFalse():
    result = generalSimilarity.sameAuthor("Maria Lilly", "Maria Li")
    assert result == 0

# Not the same author even if the last name is the same
def test_notSameAuthor():
    result = generalSimilarity.sameAuthor("Max Mustermann", "Isabell Mustermann")
    assert result == 0