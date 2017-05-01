"""
  CV_GoodFeatures demonstrates the Shi and Tomasi (1994) feature
  extractor built in to OpenCV.
"""

import cv2
import numpy as np
from cozmo_fsm import *

class CV_Edge(StateMachineProgram):
    def __init__(self):
        super().__init__(aruco=False, cam_viewer=True, annotate_cube = False)

    def start(self):
        cv2.namedWindow('features')
        dummy = numpy.array([[0]*320])
        cv2.imshow('features',dummy)

        cv2.createTrackbar('threshContour','features',170,1000,lambda self: None)
        cv2.createTrackbar('threshold1','features',1000,1000,lambda self: None)
        cv2.createTrackbar('threshold2','features',1000,1000,lambda self: None)
        cv2.createTrackbar('votes','features',25,1000,lambda self: None)

        super().start()

    def user_image(self,image,gray):
        threshContour = cv2.getTrackbarPos('threshContour', 'features')
        threshold1 = cv2.getTrackbarPos('threshold1', 'features')
        threshold2 = cv2.getTrackbarPos('threshold2', 'features')

        ret, thresholded = cv2.threshold(gray, threshContour, 255, 0)
        self.edges = cv2.Canny(thresholded, \
            threshold1, threshold2, apertureSize = 3)

    def user_annotate(self,image):
        if self.edges is None: return image
        votes = cv2.getTrackbarPos('votes', 'features')
        lines = cv2.HoughLinesP(self.edges,1,np.pi/180,votes)

        # print(self.edges[0])
        # return self.edges

        if (lines is not None):
            # for rho,theta in lines[0]:
            #     a = np.cos(theta)
            #     b = np.sin(theta)
            #     x0 = a*rho
            #     y0 = b*rho
            #     x1 = int(x0 + 1000*(-b))
            #     y1 = int(y0 + 1000*(a))
            #     x2 = int(x0 - 1000*(-b))
            #     y2 = int(y0 - 1000*(a))

            #     cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
            for line in lines:
                line = 2 * line[0]
                cv2.line(image, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 2)
        return image
