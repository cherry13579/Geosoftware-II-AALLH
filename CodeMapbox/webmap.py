from flask import Flask, render_template, url_for, request
import json
import sqlite3
import os
from osgeo import ogr

app = Flask(__name__)


@app.route("/")
@app.route("/map")
def webMap():
    return render_template("map.html")


@app.route("/getCoordinates", methods=['POST'])
def getCoordinates():
    jsdata = request.form['boundingbox']
    wktData = jsdata2wktgeo(json.loads(jsdata))
    allData = getAllDataFromPycsw()

    dataInViewport = []
    for bbox in allData:
        if boundsIntersect(wktData, bbox[1]):
            dataInViewport.append(bbox)
    
    
    return jsdata


def getAllDataFromPycsw():
    conn = sqlite3.connect(os.path.join('..', 'pycsw', 'db-data', 'data.db'))
    c = conn.cursor()
    c.execute("""   SELECT identifier, wkt_geometry
                    FROM records
                    WHERE wkt_geometry IS NOT null
            """)
    row = c.fetchall()
    return row


def boundsIntersect(wktBbox1, wktBbox2):
    print(wktBbox1, wktBbox2)
    geom1 = ogr.CreateGeometryFromWkt(wktBbox1)
    geom2 = ogr.CreateGeometryFromWkt(wktBbox2)

    return False if (geom1.Intersection(geom2)).ExportToWkt() == "GEOMETRYCOLLECTION EMPTY" else True


def jsdata2wktgeo(bbox):
    
    spatialExtent = 'POLYGON((%(minx)s %(miny)s, %(minx)s %(maxy)s, %(maxx)s %(maxy)s, %(maxx)s %(miny)s, %(minx)s %(miny)s))'
    boxData = {'minx': bbox['_sw']['lng'], 'miny': bbox['_sw']['lat'],
               'maxx': bbox['_ne']['lng'], 'maxy': bbox['_ne']['lat']}
    spatialExtent = spatialExtent % boxData
    return spatialExtent



if __name__ == "__main__":
    app.run(debug=True)
