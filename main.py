import cv2
from classes import frameAnalyzer
from config import *
import time

# # load image
# image = cv2.imread('/Users/saoron/cardiganCam/training/set6/12.png')
# frameAnalyzer.analyze_frame(image, True, False)


# load video file

cap = cv2.VideoCapture(PARENT_DIR + "/training/video/1459726324.h264.mp4")
c = 0
while True:
    # if c >0:
    #     cv2.waitKey(0)
    # c +=1
    # # print c
    if cap.grab():
        flag, frame = cap.retrieve()

        frameAnalyzer.analyze_frame(frame, True, True)

