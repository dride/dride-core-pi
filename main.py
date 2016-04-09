import cv2
from classes import frameAnalyzer


from matplotlib import pyplot as plt


# # load the image
# image = cv2.imread('/Users/saoron/cardiganCam/training/set5/frame1730.jpg')
#
# frameAnalyzer.analyze_frame(image, False, False)
#


cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw4/encoded/1459726710.h264.mp4")
while True:
    if cap.grab():
        flag, frame = cap.retrieve()

        frameAnalyzer.analyze_frame(frame, True, True)
