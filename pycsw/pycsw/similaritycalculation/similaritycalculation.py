import logging 
import os
import sqlite3
from pycsw.similaritycalculation import timeSimilarity as ts
from pycsw.similaritycalculation import spatialSimilarity as sps
from pycsw.similaritycalculation import generalSimilarity as gs

LOGGER = logging.getLogger(__name__)

# connection to the database 
conn = sqlite3.connect(os.path.join('..', '..', 'db-data', 'data.db')) 
print(conn)
c = conn.cursor()


#########################################################################
# main function of the similarity calculation 
# @author Anika Graupner 
#########################################################################
def similaritycalculation(id1, bbox, timebegin1, timeend1, format1): 

    print(id1)
    print(bbox)
    print(timebegin1)
    print(timeend1)
    print(format1)

    timeA = [timebegin1, timeend1]

    a = bbox.replace("POLYGON", "")
    b = a.replace("((", "").replace("))", "").replace(",", " ")
    bbox1 = b.split()
    print(bbox1[0])

    minx1 = bbox1[0]
    miny1 = bbox1[1]
    maxx1 = bbox1[4]
    maxy1 = bbox1[5]

    bboxA = [minx1, miny1, maxx1, maxy1]

    print(minx1, miny1, maxx1, maxy1)

    # get the title and the author of the updated record from the database 
    c.execute('SELECT title, creator FROM records WHERE identifier = '+ id +'')
    LOGGER.info('Getting title and creator from the updated record from the records table!')

    values = c.fetchall()

    title1 = values[0][0]
    creator1 = values[0][1]

    # delete all records in the similarities table where record1 or record2 is like the input id 
    c.execute('DELETE FROM similarities WHERE record1 = '+ id +' OR record2 = '+ id +'')
    LOGGER.info('Deleting records from similarities tables!')

    # select all important values from the database for similarity calculation except the values of the updated record 
    c.execute('SELECT identifier, title, time_begin, time_end, creator, wkt_geometry, format FROM records EXCEPT SELECT identifier, title, time_begin, time_end, creator, wkt_geometry FROM records WHERE identifier = '+ id +'')
    values = c.fetchall()

    rows = []
    i = 0
    while i < len(values):

        # no similarity calculation with records which have no time extend or spatial extend 
        if values[i][2] and values[i][5] is None:

            i+=1

        else:

            id2 = values[i][0]
            title2 = values[i][1]

            timebegin2 = values[i][2]
            timeend2 = values[i][3]

            timeB = [timebegin2, timeend2]

            creator2 = values[i][4]
            

            box = values[i][5]
            c = box.replace("POLYGON", "")
            d = c.replace("((", "").replace("))", "").replace(",", " ")
            bbox2 = d.split()
            print(bbox2[0])

            minx2 = bbox2[0]
            miny2 = bbox2[1]
            maxx2 = bbox2[4]
            maxy2 = bbox2[5]

            bboxB = [minx2, miny2, maxx2, maxy2]

            format2 = values[i][6]


            sameDatatype = gs.sameDatatype(format1, format2)

            sameAuthor = gs.sameAuthor(creator1, creator2)

            similarTitle = gs.similarTitle(title1, title2)

            generalSimilarity = sameDatatype + sameAuthor + similarTitle


            spatialOverlap = sps.spatialOverlap(bboxA, bboxB)

            similarArea = sps.similarArea(bboxA, bboxB)

            spatialDistance = sps.spatialDistance(bboxA, bboxB)

            spatialSimilarity = spatialOverlap + similarArea + spatialDistance


            timeLength = ts.timeLength(timeA, timeB)

            timeOverlap = ts.timeOverlap(timeA, timeB)

            timeSimilarity = timeLength + timeOverlap


            totalSimilarity = generalSimilarity + spatialSimilarity + timeSimilarity


            newrow = (str(id1), str(id2), totalSimilarity, spatialSimilarity, timeSimilarity, generalSimilarity)

            rows.append(newrow)


c.execute('insert into similarities values (record1, record2, total_similarity, geospatial_extent, temporal_extent, general_extent)', rows)

connection.commit()

LOGGER.info('Similarity calculation finished.')




