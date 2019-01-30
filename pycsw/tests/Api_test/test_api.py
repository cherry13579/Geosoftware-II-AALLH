'''
author: Aysel Tandik
Testing the API
created on: 19.12.2018
source: http://qapage.com/Testing-an-API-with-Python/
'''

import unittest
import datetime
import requests
from requests import get

class TestApi():
    SimilarRecords = 'http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=aahll:1'
    SimilarRecords2 = 'http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=aahll:1,aahll:2&similar=10&outputformat=application/json'
    SimilarityBBox = 'http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarityBBox&idone=aahll:8&idtwo=aahll:9'
    UrlWithXML = 'http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id=aahll:1,aahll:2&similar=10&outputformat=application/xml'
    UrlWithNoId = 'http://localhost:8000/?service=CSW&version=2.0.2&request=GetSimilarRecords&id='
        
    # Test--> if the schema has a json structure, or xml
    def get_response(self, test_url=SimilarRecords, format='json'):
        if format == 'json':
            response = get(test_url)
        if format == 'xml':
            response = get(test_url)

        return response.json

    def test_jsonXml_response(self):
        print('Get json Response')
        assert self.get_response(self.SimilarRecords, format='json') != 'xml'
        assert self.get_response(self.SimilarRecords2, format='json') != 'xml'
        assert self.get_response(self.SimilarityBBox, format='json') != 'xml'
        assert self.get_response(self.UrlWithXML, format='xml') != 'json'

    # Test--> if the statuscode is 200
    def test_status_response(self):
        print('Get Statuscode')
        response = requests.get(self.SimilarRecords)
        assert response.status_code == 200

        response = requests.get(self.SimilarRecords2)
        assert response.status_code == 200

        response = requests.get(self.SimilarityBBox)
        assert response.status_code == 200

    # Test--> The Timeresponse from the Url's doesnt take longer then 5000ms
    def test_time_response_Similarrecords(self):
        r = requests.get(self.SimilarRecords, timeout=6)
        r.raise_for_status()
        responseTime = str(round(r.elapsed.total_seconds(),2))
        assert responseTime < '5000'
        
    def test_time_response_SimilarBBox(self):
        r = requests.get(self.SimilarRecords2, timeout=6)
        r.raise_for_status()
        responseTime = str(round(r.elapsed.total_seconds(),2))
        assert responseTime < '5000'

        r = requests.get(self.SimilarityBBox, timeout=6)
        r.raise_for_status()
        responseTime = str(round(r.elapsed.total_seconds(),2))
        assert responseTime < '5000'

            
    # missing one id parameter, but have right content-type and right format of JSON
    def test_URL(self):
        response = requests.get(self.UrlWithNoId)
        assert response.status_code == 400
        assert response.headers['Content-Type'] == "GetSimilarRecords"
        assert self.get_response(self.UrlWithNoId, format='json') != 'xml'