import math
import logging 

LOGGER = logging.getLogger(__name__)


def sameDatatype(fileEnding1, fileEnding2):
    '''
    :author: Henry Fock
    :param fileEnding1: fileEnding of the updated record
    :param fileEnding2: fileEnding of a record in the database
    :returns: if the fileendings are the same, the function resturns the maximum value,
    else 0
    '''

    same1, same2 = -1,-1
    same1 = fileEnding1.find(fileEnding2.replace(".", "")) # 2 in 1
    same2 = fileEnding2.find(fileEnding1.replace(".", "")) # 1 in 2

    LOGGER.info('Same Datatype: %(f1)s, %(f2)s' % ({'f1' : fileEnding1, 'f2' : fileEnding2}))

    return 100 if same1>=0 or same2>=0 else 0


def similarAuthor(author1, author2):
    '''
    :author: Henry Fock
    :param author1: author / creator of the updated record
    :param author2: author / creator of a record in the database
    :returns: if the authors are the same, the function resturns the maximum value,
    else 0
    '''

    LOGGER.info('Similar Author: %(a1)s, %(a2)s' % ({'a1' : author1, 'a2' : author2}))
    return 100 if author1 == author2 else 0


def similarTitle(title1, title2):
    '''
    :author: Henry Fock
    :param title1: title of the updated record
    :param title2: title of a record in the database
    :returns: returns a value of how similar the titles of the two records are
    '''

    countList = 0
    if len(title1) >= len(title2):
        # searches for same caracters in both strings
        charList = []
        for i in title2:
            if i not in charList:
                charList.append(i)
                countList += title1.count(i)
        percent = 0
        if len(title1) != 0:
            percent = countList*100/len(title1)
            percent = math.floor(percent*100)/100
        LOGGER.info('Result similar title: %r' % (percent))
        return percent
    else:
        charList = []
        for i in title1:
            if i not in charList:
                charList.append(i)
                countList += title2.count(i)
        percent = 0
        if len(title2) != 0:
            percent = countList*100/len(title2)
            percent = math.floor(percent*100)/100
        LOGGER.info('Result similar title: %r' % (percent))
        return percent

