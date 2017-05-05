"""
  CV_GoodFeatures demonstrates the Shi and Tomasi (1994) feature
  extractor built in to OpenCV.
"""

import cv2
import numpy as np
from cozmo_fsm import *
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
    walls = [0, 0, 0]

    for line in lines:
        if isSideLine(line, 0.45, 0.85, 250):
            walls[2] = 1
        elif isSideLine(line, -0.85, -0.45, 250):
            walls[0] = 1
        elif isFrontLine(line, -0.2, 0.2, 300, 360):
            walls[1] = 1
        else: 
            continue
    return walls




class CV_Edge(StateMachineProgram):
    def __init__(self):
        super().__init__(aruco=False, cam_viewer=True, annotate_cube = False)

    def start(self):
        cv2.namedWindow('features')
        dummy = numpy.array([[0]*320])
        cv2.imshow('features',dummy)
        cv2.createTrackbar('minDistance','features',0,1000,lambda self: None)
        cv2.createTrackbar('threshContour','features',170,1000,lambda self: None)
        cv2.createTrackbar('threshold1','features',1000,1000,lambda self: None)
        cv2.createTrackbar('threshold2','features',1000,1000,lambda self: None)
        cv2.createTrackbar('votes','features',20,1000,lambda self: None)
        self.count = 0
        default_head_angle = -0.67

        if (not math.isclose(self.robot._head_angle.degrees, default_head_angle, abs_tol=1)):
            self.robot.set_head_angle(degrees(default_head_angle))

        super().start()

    def user_image(self,image,gray):

        threshContour = cv2.getTrackbarPos('threshContour', 'features')
        threshold1 = cv2.getTrackbarPos('threshold1', 'features')
        threshold2 = cv2.getTrackbarPos('threshold2', 'features')

        ret, thresholded = cv2.threshold(gray, threshContour, 255, 0)
        self.edges = cv2.Canny(thresholded, \
            threshold1, threshold2, apertureSize = 3)
        votes = cv2.getTrackbarPos('votes', 'features')
        self.lines = cv2.HoughLinesP(self.edges,1,np.pi/180,votes)


    def user_annotate(self,image):
        if self.edges is None: return image
        lines = self.lines

        if (lines is not None):
            lines = mergeLines(lines, self.count)

            walls = getWalls(lines)
            # self.parent.curWalls = walls
            print(walls)

            for line in lines:
                cv2.line(image, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 2)
        self.count = 1
        return image
