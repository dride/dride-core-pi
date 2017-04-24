import cv2
from classes import frameAnalyzer
from config import *
from classes.capture import capture
import time

# # load image
# image = cv2.imread('training/set6/1.png')
# frameAnalyzer.analyze_frame(image, True, False, True)


# load video file

cap = cv2.VideoCapture(PARENT_DIR + "/training/video/1492426327.mp4")
capture = capture(int(cap.get(3)), int(cap.get(4)))

frameNumber = 0
c = 0

while True:
    # reload config
    config = Config().getConfig()
    # if c >0:
    #     cv2.waitKey(0)
    # c +=1
    # # print c
    if cap.grab():
        flag, frame = cap.retrieve()
        frameNumber +=1
        
        # rotate 90 deg
        frame = capture.rotate_image(frame, 90)

        # start record
        if config['dvr']:
            capture.captureFrame(frame)

        frameAnalyzer.analyze_frame(frame, True, True, False, frameNumber)

