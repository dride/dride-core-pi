import cv2
from classes import frameAnalyzer
import time

from matplotlib import pyplot as plt


# load the image
image = cv2.imread('/Users/saoron/cardiganCam/training/set6/t4.jpg')
frameAnalyzer.analyze_frame(image, True, False)



# # cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw5/encoded/1460633529.h264.mp4")
# cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw6/1461659107.mp4")
# c = 0
# while True:
#     # if c >0:
#     #     cv2.waitKey(0)
#     # c +=1
#     # # print c
#     if cap.grab():
#         flag, frame = cap.retrieve()
#
#         frameAnalyzer.analyze_frame(frame, True, True)
