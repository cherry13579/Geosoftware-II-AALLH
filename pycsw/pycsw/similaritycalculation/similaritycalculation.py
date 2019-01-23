# main function of the similarity calculation 
# @author: Anika Graupner 
# @author: Henry Fock

import logging 
import os
import sqlite3

# import the calculations 
from pycsw.similaritycalculation import timeSimilarity as ts
from pycsw.similaritycalculation import spatialSimilarity as sps
from pycsw.similaritycalculation import generalSimilarity as gs

LOGGER = logging.getLogger(__name__)

def similaritycalculation(id1, bbox, timebegin1, timeend1, format1):
    '''
    Main function of the similarity calculation.
    Runs the functions for the similarity calculations.
    :authors: Anika Graupner, Henry Fock
    :param id1: Identifier of the udated record
    :param bbox: Bbox of the updated record 
    :param timebegin1: timebegin of the updated record
    :param timeend1: timeend of the updated record
    :param format1: fileformat of the uodated record
    ''' 

    LOGGER.info('Similaritycalculation started.')

    print(timebegin1)
    print(timeend1)

    # connection to the database 
    conn = sqlite3.connect(os.path.join('..', '..', 'db-data', 'data.db')) 
    LOGGER.debug(conn)
    c = conn.cursor()

    # test if there is only one record in the database
    # if yes, the calculation will not run
    c.execute("SELECT identifier FROM records")
    values = c.fetchall()
    if len(values) > 1:

        # formatting the input for the functions of the timeSimilarity
        timeA = [timebegin1, timeend1]
        
        # formatting the input for the functions of the spatialSimilarity
        a = bbox.replace("POLYGON", "")
        b = a.replace("((", "").replace("))", "").replace(",", " ")
        bbox1 = b.split()

        minx1 = bbox1[0]
        miny1 = bbox1[1]
        maxx1 = bbox1[4]
        maxy1 = bbox1[5]

        bboxA = [minx1, miny1, maxx1, maxy1]
        bboxA = list(map(float, bboxA))

        bboxA = [124.99553571, 67.99553636, 165.00445788, 72.00446429]

        # get the title and the author of the updated record from the database 
        c.execute("SELECT title, creator FROM records WHERE identifier = %r" % (id1))
        LOGGER.info('Getting title and creator from the updated record from the records table!')

        values = c.fetchall()

        title1 = values[0][0]
        creator1 = values[0][1]

        # delete all records in the similarities table where record1 or record2 is like the input id 
        c.execute("DELETE FROM similarities WHERE record1 = %(id1)r OR record2 = %(id1)r" % ({'id1' : id1}))
        conn.commit()
        LOGGER.info('Deleting records from similarities tables!')


        # select all important values from the database for similarity calculation except the values of the updated record 
        c.execute("SELECT identifier, title, time_begin, time_end, creator, wkt_geometry, format FROM records WHERE NOT identifier = %r" % (id1))
        values = c.fetchall()

        rows = []
        # for each record in the database
        i = 0
        while i < len(values):

            # the record should not be compared to itself
            if values[i][0] is id1:

                i+=1

            # no similarity calculation with records which have no time extend or no spatial extend 
            if values[i][2] and values[i][5] is None:

                i+=1

            # start comparing the updated record with all valid records in the database
            else:

                # formatting the variables of the respective record
                id2 = values[i][0]
                title2 = values[i][1]
                timebegin2 = values[i][2]
                timeend2 = values[i][3]
                timeB = [timebegin2, timeend2]
                creator2 = values[i][4]
                box = values[i][5]
                e = box.replace("POLYGON", "")
                d = e.replace("((", "").replace("))", "").replace(",", " ")
                bbox2 = d.split()
                minx2 = bbox2[0]
                miny2 = bbox2[1]
                maxx2 = bbox2[4]
                maxy2 = bbox2[5]
                bboxB = [minx2, miny2, maxx2, maxy2]
                bboxB = list(map(float, bboxB))
                bboxB = [124.99553571, 67.99553636, 165.00445788, 72.00446429]
                format2 = values[i][6]

                
                # general similarity (same dataformat, same author, similar title)
                sameDatatype = gs.sameDatatype(format1, format2) 
                similarAuthor = gs.similarAuthor(creator1, creator2) 
                similarTitle = gs.similarTitle(title1, title2) 

                generalSimilarity = sameDatatype + similarAuthor + similarTitle 
                #LOGGER.info('General similarity for format1 '+ format1 +' and format2 '+ format2 +': '+ generalSimilarity + '.')

                # spatial simialrity (overlapping bboxes, similar area of the bboxes, spatial distance)
                spatialOverlap = sps.spatialOverlap(bboxA, bboxB) 
                similarArea = sps.similarArea(bboxA, bboxB) 
                spatialDistance = sps.spatialDistance(bboxA, bboxB) 

                spatialSimilarity = spatialOverlap + similarArea + spatialDistance 
                #LOGGER.info('Spatail similarity for bboxA '+ bboxA +' and bboxB '+ bboxB +': '+ spatialSimilarity + '.')

                # temporal similarity (time length, overlapping of the time periods)
                timeLength = ts.timeLength(timeA, timeB) 
                timeOverlap = ts.timeOverlap(timeA, timeB) 

                timeSimilarity = timeLength + timeOverlap 
                #LOGGER.info('Time similarity for timeA '+ timeA +' and timeB '+ timeB +': '+ timeSimilarity + '.')

                # add everything together for the total similarity value
                totalSimilarity = generalSimilarity + spatialSimilarity + timeSimilarity
                #LOGGER.info('Total similarity for dataset '+ id1 +' and dataset '+ id2 +': '+ timeSimilarity + '.')

                # new tupel add to rows list (later inserted in the database table similarities)
                newrow = (id1, id2, totalSimilarity, spatialSimilarity, timeSimilarity, generalSimilarity)
                rows.append(newrow)

                i+=1

        LOGGER.debug(rows)

        # insert the calculated values into the database 
        for entry in rows:

            sql = """insert into similarities (record1, record2, total_similarity, geospatial_extent, temporal_extent, general_extent) 
                    values (?,?,?,?,?,?)"""

            c.execute(sql, entry)
            conn.commit()

        LOGGER.info('Similarity calculation finished.')
    
    else:
        LOGGER.info('Nothing to compare.')




