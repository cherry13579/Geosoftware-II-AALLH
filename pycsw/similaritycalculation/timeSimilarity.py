from math import floor
from DateTime import DateTime
import logging

LOGGER = logging.getLogger(__name__)
#LOGGER.info()
#LOGGER.debug()
#LOGGER.warning()

def timeLength(timeA, timeB):
    """calculates how similar two timelines are in length (len(timeA)/len(timeB) where timeA >= timeB)
    :param timeA [start, end] list with start and end date
    :param timeB [start, end] list with start and end date
    :returns: value [0,1] of how much the two lengths are similar
    """
    startA = DateTime(timeA[0])
    endA = DateTime(timeA[1])

    startB = DateTime(timeB[0])
    endB = DateTime(timeB[1])

    # check if values are invalid or if an end date is before its start date
    if startA > endA or startB > endB:
        raise AttributeError("start value is higher than end value")

    # get timelength of timeA and timeB (calculation is done automaticly by DateTime)
    lengthA = endA - startA
    lengthB = endB - startB

    # prevent division by zero if both times have length 0
    if lengthA == lengthB:
        return 1
    # calculate similarity
    else:
        if lengthA > lengthB:
            lengthPercentage = lengthB/lengthA
            return lengthPercentage
        else:
            lengthPercentage = lengthA/lengthB
            return lengthPercentage

def timeOverlap(timeA, timeB):
    """calculates how much timeA and timeB overlap eachother
    :param timeA [start, end] list with start and end date
    :param timeB [start, end] list with start and end date
    :returns: percentage of overlap
    """
    # calculate the overlapping time
    if DateTime(timeA[0]) == DateTime(timeB[0]) and DateTime(timeA[1]) == DateTime(timeB[1]):
        # timeA and timeB are equal
        return 1

    # start A below start B
    if DateTime(timeA[0]) <= DateTime(timeB[0]):
        if DateTime(timeA[1]) <= DateTime(timeB[0]):
            # no overlap, because end A below or on start B
            return 0
        else: # overlap
            overlap = DateTime(timeA[1]) - DateTime(timeB[0])

    else: # start B below start A
        if DateTime(timeB[1]) <= DateTime(timeA[0]):
            # no overlap, because end B below or on start A
            return 0
        else: # overlap
            overlap = DateTime(timeB[1]) - DateTime(timeA[0])
    
    # calculate timelength of timeA and timeB (calculation done by DateTime)
    timeLengthA = DateTime(timeA[1]) - DateTime(timeA[0])
    timeLengthB = DateTime(timeB[1]) - DateTime(timeB[0])

    # prevent division by zero by giving a single moment a duration of arround a second
    if timeLengthA == 0:
        timeLengthA = 0.00001
    if timeLengthB == 0:
        timeLengthB = 0.00001

    # calculate percentage of overlap (overlap/longer time sequence)
    if timeLengthA > timeLengthB:
        overlapPercentage = overlap/timeLengthA
        return overlapPercentage
    else:
        overlapPercentage = overlap/timeLengthB
        return overlapPercentage

# def similarInterval(timeA, timeB):
#     if timeA[2] == timeB[2]:
#         return 1
#     else:
#         if timeA[2] > timeB[2]:
#             intervalPercentage = timeB[2]/timeA[2]
#             intervalPercentage = floor(intervalPercentage*100)/100
#             return intervalPercentage
#         else:
#             intervalPercentage = timeA[2]/timeB[2]
#             intervalPercentage = floor(intervalPercentage*100)/100
#             return intervalPercentage