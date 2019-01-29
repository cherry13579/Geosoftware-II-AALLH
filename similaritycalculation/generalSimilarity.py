import math
import logging

LOGGER = logging.getLogger(__name__)

def sameDatatype(fileEnding1, fileEnding2):
    """checks if two datatypes are the same or from same family
    :param fileEnding1 String for instance ".tiff"
    :param fileEnding2 String for instance ".geotiff"
    :returns: 1 if they are the same, otherwise 0
    """
    same1, same2 = -1,-1
    same1 = fileEnding1.find(fileEnding2.replace(".", "")) # 2 in 1
    same2 = fileEnding2.find(fileEnding1.replace(".", "")) # 1 in 2

    LOGGER.info("Datatypes %s and %s" % (fileEnding1, fileEnding2))
    return 1 if same1>=0 or same2>=0 else 0

def sameAuthor(author1, author2):
    """checks if two Authors are the same
    :param author1 String with Author
    :param author2 String with Author
    :returns: 1 if they are the same, otherwise 0
    """
    LOGGER.info("Authors %s and %s" % (author1, author2))
    return 1 if author1 == author2 else 0

def similarTitle(title1, title2):
    """checks if two strings are similar in reference to an amount of same characters
    :param title1 String the first title
    :param title2 String the second title
    :returns: number between 1 and 0
    """
    LOGGER.info("Titles %s and %s" % (title1, title2))
    countList = 0
    if len(title1) >= len(title2):
        # searches for same caracters in both strings
        charList = []
        for i in title2:
            # check if char has already been found
            if i not in charList:
                charList.append(i)
                # count how often the char appears in the other string
                countList += title1.count(i)
        LOGGER.info("List of same characters: " + str(charList))

        percent = 0
        if len(title1) != 0:
            percent = countList/len(title1)
        return percent

    else:
        charList = []
        for i in title1:
            if i not in charList:
                charList.append(i)
                countList += title2.count(i)
        LOGGER.info("List of same characters: " + str(charList))
        
        percent = 0
        if len(title2) != 0:
            percent = countList/len(title2)
        return percent