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

        cv2.createTrackbar('threshold1','features',10,1000,lambda self: None)
        cv2.createTrackbar('threshold2','features',10,1000,lambda self: None)

        super().start()

    def user_image(self,image,gray):
        threshold1 = cv2.getTrackbarPos('threshold1', 'features')
        threshold2 = cv2.getTrackbarPos('threshold2', 'features')
        self.edges = cv2.Canny(gray, threshold1, threshold2, apertureSize = 3)

    def user_annotate(self,image):
        if self.edges is None: return image
        lines = cv2.HoughLines(self.edges,1,np.pi/180,25)

        if (lines != None):
            for rho,theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))

                cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        return image
