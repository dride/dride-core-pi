import cv2
from classes import frameAnalyzer
import time

from matplotlib import pyplot as plt


# # load the image
# image = cv2.imread('/Users/saoron/cardiganCam/training/set6/18.png')
# frameAnalyzer.analyze_frame(image, True, False)



cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw4/encoded/1459726084.h264.mp4")
c = 0
while True:
    # if c >0:
    #     cv2.waitKey(0)
    # c +=1
    # print c
    if cap.grab():
        flag, frame = cap.retrieve()

        frameAnalyzer.analyze_frame(frame, True, True)
