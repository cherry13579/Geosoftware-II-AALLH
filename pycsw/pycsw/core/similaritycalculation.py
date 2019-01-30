import logging 
import os
import sqlite3
from math import floor 
from pycsw.core import timeSimilarity as ts
from pycsw.core import spatialSimilarity as sps
from pycsw.core import generalSimilarity as gs

LOGGER = logging.getLogger(__name__)

def similaritycalculation(id1):
    '''
    Main function of the similarity calculation.
    Runs the functions for the similarity calculations.
    @authors Anika Graupner, Henry Fock
    :param id1: Identifier of the udated or inserted record
    ''' 

    LOGGER.info('Similaritycalculation started.')

    # connection to the database 
    conn = sqlite3.connect(os.path.join('db-data', 'data.db')) 
    c = conn.cursor()

    # test if there is only one record in the database
    # if yes, the calculation will not run
    c.execute("SELECT identifier FROM records")
    numberrec = c.fetchall()
    
    if len(numberrec) > 1:

        # get the the important values of the updated or inserted record 
        c.execute("SELECT title, time_begin, time_end, creator, wkt_geometry, format FROM records WHERE identifier = %r" % (id1))
        LOGGER.info('Getting the the important values of the updated or inserted record')
        valuesrec1 = c.fetchall()
 
        

        title1 = valuesrec1[0][0]
        creator1 = valuesrec1[0][3]
        format1 = valuesrec1[0][5]
        bbox = valuesrec1[0][4]
        timebegin1 = valuesrec1[0][1]
        timeend1 = valuesrec1[0][2]

        # formatting the bbox of the updated or inserted record if there is one 
        if valuesrec1[0][4]:

            # formatting bbox and timeextent of the updated or inserted record
            a = bbox.replace("POLYGON", "")
            b = a.replace("((", "").replace("))", "").replace(",", " ")
            bbox1 = b.split()
            minx1 = bbox1[0]
            miny1 = bbox1[1]
            maxx1 = bbox1[4]
            maxy1 = bbox1[5]
            bboxA = [minx1, miny1, maxx1, maxy1]
            bboxA = list(map(float, bboxA))
    
        else:

            LOGGER.info('The updated or inserted record %r has no bbox.' % (id1))
                        
        # formatting the timeextend of the updated or inserted record if there is one 
        if valuesrec1[0][1]:

            timeA = [timebegin1, timeend1]
        
        else:

            LOGGER.info('The updated or inserted record %r has no time extent.' % (id1))
            
        # delete all records in the similarities table where record1 or record2 is like the input id 
        # this is important when a record will be updated twice or more 
        c.execute("DELETE FROM similarities WHERE record1 = %(id1)r OR record2 = %(id1)r" % ({'id1' : id1}))
        conn.commit()
        LOGGER.info('Deleting records from similarities tables!')

        # select all important values from the database for similarity calculation except the values of the updated or inserted record, because the 
        # updated value will not be compared with hisself 
        c.execute("SELECT identifier, title, time_begin, time_end, creator, wkt_geometry, format FROM records")
        LOGGER.info('Getting important values from the database for similarity calculation except the values of the updated or inserted record')
        values = c.fetchall()
        
        # for each record in the database (except the record with the id of the updated or inserted record)
        rows = []
        i = 0
        while i < len(values):
            if values[i][0] == id1:
                i+=1
            
            # start comparing the updated or inserted record with all valid records in the database
            else:
                
                # id of the respective record in the database
                id2 = values[i][0]
                
                # weights for the total similarity of the similarity calculation
                weight = {
                    "space" : {
                        "isg" : 45,
                        "overlap" : 20,
                        "area" : 15,
                        "distance" : 10
                    },
                    "time" : {
                        "isg" : 30,
                        "length" : 15,
                        "overlap" : 15
                    },
                    "general" : {
                        "isg" : 25,
                        "type" : 10,
                        "author" : 5,
                        "title" : 10
                    }
                }

                # test if both records have a timeextent
                if values[i][2] and timebegin1:
                    
                    # formatting the input for the functions of the timeSimilarity
                    timeB = [values[i][2], values[i][3]]

                    # temporal similarity (time length, overlapping of the time periods)
                    timeLength = ts.timeLength(timeA, timeB)*weight["time"]["length"]
                    timeOverlap = ts.timeOverlap(timeA, timeB)*weight["time"]["overlap"] 

                    timeSimilarity = timeLength + timeOverlap                    
                
                # if not it is not necessary to run the functions for the time similarity and the timeSimilarity is 0
                else:
                    
                    timeSimilarity = 0 

                # test if both records have a spatial extent
                if bbox and values[i][5]:
                    
                    # formatting bbox of the repective record in the database 
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

                    # spatial simialrity (overlapping bboxes, similar area of the bboxes, spatial distance)
                    spatialOverlap = sps.spatialOverlap(bboxA, bboxB)*weight["space"]["overlap"]
                    similarArea = sps.similarArea(bboxA, bboxB)*weight["space"]["area"]
                    spatialDistance = sps.spatialDistance(bboxA, bboxB)*weight["space"]["distance"]

                    spatialSimilarity = spatialOverlap + similarArea + spatialDistance

                # if not it is not necessary to run the functions for the spatial similarity and the spatialSimilarity is 0
                else:
                    spatialSimilarity = 0
                
                # test if both records have a title
                if title1 and values[i][1]:
                    
                    title2 = values[i][1]
                    similarTitle = gs.similarTitle(title1, title2)*weight["general"]["title"]
                
                # if not it is not necessary to run the functions for the similar Title and similarTitle is 0
                else:

                    similarTitle = 0
                
                # test if both records have a creator
                if creator1 and values[i][4]:

                    creator2 = values[i][4]
                    sameAuthor = gs.sameAuthor(creator1, creator2)*weight["general"]["author"]
                
                # if not it is not necessary to run the functions for the same Author and sameAuthor is 0
                else:
                    
                    sameAuthor = 0
                
                # test if both records have a format
                if format1 and values[i][6]:

                    format2 = values[i][6]
                    sameDatatype = gs.sameDatatype(format1, format2)*weight["general"]["type"]

                # if not it is not necessary to run the functions for the same datatype and sameDatatype is 0
                else:
                    
                    sameDatatype = 0

                # calculate the general similarity 
                generalSimilarity = sameDatatype + sameAuthor + similarTitle
                
                # add everything together for the total similarity value
                # /100 because we want to have values between 0 and 1
                totalSimilarity = (generalSimilarity + spatialSimilarity + timeSimilarity)/100

                # new tupel add to rows list (later inserted in the database table similarities)
                newrow = (id1, id2, round(totalSimilarity, 4), round(spatialSimilarity/weight["space"]["isg"], 4), 
                    round(timeSimilarity/weight["time"]["isg"], 4), round(generalSimilarity/weight["general"]["isg"], 4))

                rows.append(newrow)
                
                LOGGER.debug(newrow)
                
                i+=1
        
        # insert the calculated values into the database 
        for entry in rows:
        
            sql = """insert into similarities (record1, record2, total_similarity, geospatial_extent, temporal_extent, general_extent) 
                    values (?,?,?,?,?,?)"""

            c.execute(sql, entry)
            conn.commit()

        LOGGER.info('Similarity calculation finished.')
            
    # if there was only one value in the database 
    else:
        LOGGER.info('Nothing to compare.')




