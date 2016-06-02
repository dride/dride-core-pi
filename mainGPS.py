import cv2
from classes import frameAnalyzer
from config import *
from classes.capture import capture
from classes.gps import GPS
import time

# # load image
# image = cv2.imread('training/set6/1.png')
# frameAnalyzer.analyze_frame(image, True, False, True)


# load video file
filename = '1464525420'


gps = GPS()
cap = cv2.VideoCapture(PARENT_DIR + "/training/wGPS/clip/"+filename+".avi")
capture = capture(int(cap.get(3)), int(cap.get(4)))
start = time.clock()
c = 0
while True:
    # if c >0:
    #     cv2.waitKey(0)
    c +=1
    # # print c
    if cap.grab():
        gps.updateSystemPositionData(int(time.clock() - start), filename)

        flag, frame = cap.retrieve()

        frameAnalyzer.analyze_frame(frame, True, True)

