import os
import sqlite3


# connection to the database 
conn = sqlite3.connect(os.path.join('..', '..', 'db-data', 'data.db')) 
print(conn)
c = conn.cursor()


#########################################################################
# main function of the similarity calculation 
# @author Anika Graupner 
#########################################################################
def similaritycalculation(id, bbox, timebegin, timeend, format): 

    print(id)
    print(bbox)
    print(timebegin)
    print(timeend)
    print(format)

    # select all important values from the database for similarity calculation except the values of the updated record 
    c.execute('SELECT identifier, title, time_begin, time_end, creator, wkt_geometry FROM records EXCEPT SELECT identifier, title, time_begin, time_end, creator, wkt_geometry FROM records WHERE identifier = '+ id +'')
    values = c.fetchall()
    print(values)
    print(values[0][4])

    if values[0][4] is None:
        print('none')

    # rows = []
    # i = 0
    # while i < len(values):

        # no similarity calculation with records which have no time extend or spatial extend 
        # if values[i][2] || values[i][3] || values[i][5 ]is None:

        #     i++

        
        #else:

            # hier müssen wir jetzt absprechen, wie die Daten formatiert sein müssen für die Berechnungen 
            # dann wird das für jeden Datensatz durchlaufen und in eine Liste eingefügt, diese wird dann am Ende komplett in die DB eingefügt
                # die einzelnen returns noch zusammen rechnen aber auch einzeln speichern (siehe insert unten)
            # wir müssen noch das mit den Modulen klären, dafür ist wichtig, wie der ganze Kram nachher auf Docker geladen wird 
            # WAS WENN DER GLEICHE DATENSATZ NOCHMAL ABGEDATED WIRD, vorher checken, ob es den primärschlüssel in der similarity tabelle schon gibt 


# INSERT
# rows = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#         ('2006-04-05', 'BUY', 'MSOFT', 1000, 72.00),
#         ('2006-04-06', 'SELL', 'IBM', 500, 53.00)]
# c.execute('insert into similarities values (record1, record2, total_similarity, geospatial_extent, temporal_extent, dataformat, title, author, bbox)', rows)
# connection.commit()




