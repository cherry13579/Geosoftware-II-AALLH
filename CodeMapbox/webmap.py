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
    jsdata = request.form['boundingbox']
    # print(jsdata)
    wktData = jsdata2wktgeo(json.loads(jsdata))
    allData = getAllDataFromPycsw()
    dataInViewport = []
    for bbox in allData:
        if bound1InBound2(wktData, bbox['bbox']):
            dataInViewport.append(bbox)

    if not dataInViewport:
        return json.dumps({'status': 'OK', 'table': "<tr><th>No data available for this region!</th></tr>", 'bboxen': None})
    table = createTable(dataInViewport)
    jsonBox = wkt2json(dataInViewport)
    return json.dumps({'status': 'OK', 'table': table, 'bboxen': jsonBox})
    # return "hallo"


def getAllDataFromPycsw():
    conn = sqlite3.connect(os.path.join('..', 'pycsw', 'db-data', 'data.db'))
    c = conn.cursor()
    c.execute("""   SELECT identifier, wkt_geometry, title, time_begin, time_end, creator
                    FROM records
                    WHERE wkt_geometry IS NOT null
            """)
    row = c.fetchall()

    # print(row)
    row = list(map(lambda a: {"ID": a[0], 'Creator': a[5], 'Title': a[2],
                              'Time begin': a[3], 'Time end': a[4], "bbox": a[1]}, row))
    return row


def bound1InBound2(wktBbox1, wktBbox2):
    geom1 = ogr.CreateGeometryFromWkt(wktBbox1)
    geom2 = ogr.CreateGeometryFromWkt(wktBbox2)

    # print(geom1.Contains(geom2))

    return geom1.Contains(geom2)


def jsdata2wktgeo(bbox):
    spatialExtent = 'POLYGON((%(minx)s %(miny)s, %(minx)s %(maxy)s, %(maxx)s %(maxy)s, %(maxx)s %(miny)s, %(minx)s %(miny)s))'
    boxData = {'minx': bbox['_sw']['lng'], 'miny': bbox['_sw']['lat'],
               'maxx': bbox['_ne']['lng'], 'maxy': bbox['_ne']['lat']}
    spatialExtent = spatialExtent % boxData
    return spatialExtent


def wkt2json(wktGeometryList):
    listOfBboxesList = list(map(lambda b: ((float(b[0][0]), float(b[0][1]), float(b[0][4]), float(b[0][5])), b[1]), map(lambda a: (a['bbox'].replace("POLYGON", "").replace(
        "((", "").replace("))", "").replace(",", " ").split(), a['ID']), wktGeometryList)))

    def toJson(data):
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

    jsonBboxes = list(map(toJson, listOfBboxesList))

    return jsonBboxes


def createTable(values):
    tableMain = """
    <tr>
        %(heading)s
    </tr>
    %(content)s
    """

    keys = [x for x in values[0].keys()]
    headings = ""
    for key in keys:
        headings += "<th>%s</th>" % key

    content = ""
    for dataset in values:
        content += "<tr>\n"
        for key in keys:
            content += "    <td>%s</td>\n" % dataset[key]
        content += "</tr>\n"

    table = tableMain % {"heading": headings, "content": content}

    return table


if __name__ == "__main__":
    app.run(debug=True)
