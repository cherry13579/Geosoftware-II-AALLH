'''
Created on 20.01.2019
@author: Henry Fock
'''

from flask import Flask, render_template, url_for, request, redirect, session
import json
import sqlite3
import os
from osgeo import ogr

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route("/")
@app.route("/map")
def webMap():
    return render_template("map.html")


@app.route("/getCoordinates", methods=['POST'])
def getCoordinates():
    """Get geometry data from JavaScript and proccess it
    """
    # get the data send by JavaScript
    jsdata = request.form['boundingbox']

    # check if retrieved data is from viweport button or from draw button
    if "type" in json.loads(jsdata).keys():
        jsonData = json.loads(jsdata)
        # print(jsonData)
    else:
        jsonData = jsdata2geojson(json.loads(jsdata))
        # print(jsonData)

    # get all data from pycsw an filter for bboxes within specified areas
    allData = getAllDataFromPycsw()
    dataInViewport = []
    for bbox in allData:
        if bound1InBound2(jsonData, bbox['bbox']):
            dataInViewport.append(bbox)

    # If there is no data in selected region
    if not dataInViewport:
        return json.dumps({'status': 'OK', 'table': "<tr><th>No data available for this region!</th></tr>", 'bboxen': None})

    # create a table with data from pycsw
    table = createTable(dataInViewport)
    # get the bboxes to display them on the map
    jsonBox = wkt2json(dataInViewport)
    return json.dumps({'status': 'OK', 'table': table, 'bboxen': jsonBox})


def getAllDataFromPycsw():
    """Get all Data from pycsw database
    :returns: a list of dicts including the selectrd data from pycsw
    """
    conn = sqlite3.connect(os.path.join('..', 'pycsw', 'db-data', 'data.db'))
    c = conn.cursor()
    c.execute("""   SELECT identifier, wkt_geometry, title, time_begin, time_end, creator
                    FROM records
                    WHERE wkt_geometry IS NOT null
            """)
    row = c.fetchall()
    # convert to a list of dicts
    row = list(map(lambda a: {"ID": a[0], 'Creator': a[5], 'Title': a[2],
                              'Time begin': a[3], 'Time end': a[4], "bbox": a[1]}, row))
    return row


def bound1InBound2(jsonPolygon, wktBbox):
    """checks if the second parameter is spatialy within the first parameter
    :param jsonPolygon search area
    :param wktBbox bbox to be checked
    :returns: True if jsonPolygon CONTAINS wktBbox
    """
    if "FeatureCollection" in jsonPolygon.values():
        geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
        for feature in jsonPolygon["features"]:
            geometry = feature["geometry"]
            ogrGeometry = ogr.CreateGeometryFromJson(json.dumps(geometry))
            geomcol.AddGeometry(ogrGeometry)
        
        geom1 = geomcol
    
    else:
        geom1 = ogr.CreateGeometryFromJson(json.dumps(jsonPolygon))

    geom2 = ogr.CreateGeometryFromWkt(wktBbox)

    return geom1.Contains(geom2)


def jsdata2geojson(jsdata):
    """Converts the viewportBoudingbox from MapBox to a GeoJSON
    :param jsdata Viewport bbox from MapBox
    :returns: the Viewport bbox from MapBox as GeoJSON Feature
    """
    geojson = """
    {
        "type": "Polygon",
        "coordinates": [
            [
                [%(minx)f, %(miny)f],
                [%(minx)f, %(maxy)f],
                [%(maxx)f, %(maxy)f],
                [%(maxx)f, %(miny)f],
                [%(minx)f, %(miny)f]
            ]
        ]
        
    }"""

    boxData = {'minx': jsdata['_sw']['lng'], 'miny': jsdata['_sw']['lat'],
               'maxx': jsdata['_ne']['lng'], 'maxy': jsdata['_ne']['lat']}
    geojson = geojson % boxData
    return json.loads(geojson)


def wkt2json(wktGeometryList):
    """converts a list of WKT-Geometrys (Boudingbox) to a list of GeoJSON geometries
    :param wktGeometryList List containing WKT-Geometry boundingboxes and their ID
    :returns: list of GeoJSON boudingboxes with their HTML ID as property and an empty color property
    """
    # first it removes all unnecessary text from each entry in wktGeometryList.
    # and secondly it creates a tuple with ((minx,miny,maxx,maxy), ID)
    listOfBboxesList = list(map(lambda b: ((float(b[0][0]), float(b[0][1]), float(b[0][4]), float(b[0][5])), b[1]), map(lambda a: (a['bbox'].replace("POLYGON", "").replace(
        "((", "").replace("))", "").replace(",", " ").split(), a['ID']), wktGeometryList)))

    def toJson(data):
        """small method to place the data from listOfBboxesList in a GeoJSON
        :param data entry from listOfBboxesList
        :returns: GeoJSON
        """
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [data[0][0], data[0][1]],
                        [data[0][0], data[0][3]],
                        [data[0][2], data[0][3]],
                        [data[0][2], data[0][1]],
                        [data[0][0], data[0][1]]
                    ]
                ]
            },
            "properties": {
                "ID": "<b>ID: %s</b>" % data[1],
                "color": None
            },
        }
    # convert all entrys from listOfBboxesList to GeoJSON
    jsonBboxes = list(map(toJson, listOfBboxesList))

    return jsonBboxes


def createTable(values):
    """Creates a table from a list of one dimensional dicts. Keys of the first dict will be used as headings.
    :param values list woth dicts that only have one layer of dicts (subdicts lead to ugly results)
        and each dict needs to have the same keys or they won't be displayed or an error will be raised
    :returns: HTML table content that can be put into a HTML table tag
    """
    # table body
    tableMain = """
    <tr>
        %(heading)s
    </tr>
    %(content)s
    """

    # get all the keys from
    keys = [x for x in values[0].keys()]
    headings = ""
    for key in keys:
        headings += "<th>%s</th>" % key

    content = ""
    try:
        for dataset in values:
            content += "<tr>\n"
            for key in keys:
                if key == "bbox":
                    content += "    <td class='bbox'>%s</td>\n" % dataset[key]
                else:
                    content += "    <td>%s</td>\n" % dataset[key]
            content += "</tr>\n"
    except KeyError as e:
        raise KeyError("dicts must have the same keys")

    table = tableMain % {"heading": headings, "content": content}

    return table


if __name__ == "__main__":
    app.run(debug=False)