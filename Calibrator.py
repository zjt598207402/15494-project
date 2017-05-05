import cv2
import numpy as np
import math

def lineDistance(line):
    return distance((line[0], line[1]), (line[2], line[3]))

def distance(pointA, pointB):
    aX = pointA[0]
    aY = pointA[1]
    bX = pointB[0]
    bY = pointB[1]

    return math.sqrt(math.pow((bX - aX), 2) + math.pow((bY - aY), 2))

def slope(line):
    if (line[2] - line[0] == 0):
        return 1
    else:
        output = ((line[3] - line[1]) / (line[2] - line[0]))
        return output
 
def isNear(pointA, pointB):
    maxDistance = 5

    aX = pointA[0]
    aY = pointA[1]
    bX = pointB[0]
    bY = pointB[1]

    ptDistance = distance(pointA, pointB)

    if ptDistance > 5:
        return False

    return True


def isSameSlope(lineA, lineB, count):
    maxDif = 0.15

    slopeA = slope(lineA)
    slopeB = slope(lineB)

    slopeDif = slopeA - slopeB

    if (slopeDif > maxDif or slopeDif < -maxDif):
        return False
    
    return True


def mergeLines(lines, count):
    outputs = []
    minDistance = cv2.getTrackbarPos('minDistance', 'features')

    for line in lines:

        line = 2 * line[0]

        if len(outputs) == 0:
            outputs.append(line)
        else:
            for i in range(len(outputs)):
                output = outputs[i]

                if not isSameSlope(line, output, count):
                    continue
                else:
                    line1p1 = (output[0], output[1])
                    line1p2 = (output[2], output[3])

                    line2p1 = (line[0], line[1])
                    line2p2 = (line[2], line[3])

                    if isNear(line1p2, line2p1):
                        outputs[i] = [output[0], output[1], line[2], line[3]]
                        break
                    elif isNear(line2p2, line1p1):
                        outputs[i] = [line[0], line[1], output[2], output[3]]
                        break
                    # elif isNear(line2p1, line1p1):
                    #     outputs[i] = [output[2], output[3], line[2], line[3]]
                    # elif isNear(line2p2, line1p2):
                    #     outputs[i] = [output[0], output[1], line[0], line[1]]
                    else:
                        continue

            outputs.append(line)

    returnOutput = []
    for output in outputs:
        if(lineDistance(output) > minDistance):
            returnOutput.append(output)

    return returnOutput

def getMinY(line):
    return min(line[1], line[3])

def getMaxY(line):
    return max(line[1], line[3])

def isFrontLine(line, slopeMin, slopeMax, minY, maxY):
    lineSlope = slope(line)
    # print(line)
    # print(lineSlope)
    # print()
    lineMaxY = getMaxY(line)

    if lineSlope > slopeMin and lineSlope < slopeMax \
        and lineMaxY <= maxY and lineMaxY >= minY:
        return True
    return False

def isSideLine(line, slopeMin, slopeMax, minY):
    lineSlope = slope(line)
    # print(line)
    # print(lineSlope)
    # print()
    if lineSlope > slopeMin and lineSlope < slopeMax \
        and getMinY(line) >= minY:
        return True
    return False

def getWalls(lines):
    walls = [(0,True), (0,True), (0, True)]

    for line in lines:
        if isFrontLine(line, -0.2, 0.2, 0, 200):
            walls[1] = (0, False)
        elif isSideLine(line, 0.45, 0.85, 250):
            walls[2] = (1, True)
        elif isSideLine(line, -0.85, -0.45, 250):
            walls[0] = (1, True)
        elif isFrontLine(line, -0.2, 0.2, 300, 375):
            (wall, canChange) = walls[1]
            if (canChange):
                walls[1] = (1, True)
        else: 
            continue

    output = []

    for (wall,canChange) in walls:
        output.append(wall) 

    return output

# def getFrontDistance(lines):
#     midY = -1

#     for line in lines:
#         if isFrontLine(line, -0.2, 0.2, 300, 360):
#             