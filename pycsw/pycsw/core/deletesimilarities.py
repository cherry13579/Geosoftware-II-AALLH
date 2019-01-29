import logging 
import os
import sqlite3

LOGGER = logging.getLogger(__name__)

def deleteSimilarities(id, constraint):
    '''
    Function which deletes the respective records in the similarities table 
    when a user runs a delete transaction
    @author: Anika Graupner 
    :param id: id of the deleted record in the delete transaction 
    '''

    LOGGER.info('DeleteSimilarities is running for the record with the id %r' % (id))

    # connection to the database 
    conn = sqlite3.connect(os.path.join('db-data', 'data.db')) 
    LOGGER.debug(conn)
    c = conn.cursor()

    c.execute("SELECT record1, record2 FROM similarities WHERE record1 = %(id)r OR record2 = %(id)r" % ({'id' : id}))
    values = c.fetchall()

    # if a user does a delete all transaction 
    if str(id) is '%' and '@wildCard' in constraint['_dict']['ogc:Filter']['ogc:PropertyIsLike']:

        c.execute("DELETE FROM similarities")
        conn.commit()
        LOGGER.info("Deleting all records from similarities table.")

    elif values:

        # delete all records in the similarities table where record1 or record2 is like the input id 
        c.execute("DELETE FROM similarities WHERE record1 = %(id)r OR record2 = %(id)r" % ({'id' : id}))
        conn.commit()
        LOGGER.info('Deleting records from similarities tables where record1 or record2 is %r!' % (id))
    
    else:
        LOGGER.info('Nothing to delete.')
