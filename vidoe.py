# import the necessary packages
import numpy as np
import cv2
import math
import os

from matplotlib import pyplot as plt


def getColorByAngle(angle):

    if (angle > 10 and angle <= 15):
        return (245, 12, 12)
    if (angle > 15 and angle <= 25):
        return (245, 12, 184)
    if (angle > 25 and angle <= 35):
        return (134, 12, 245)
    if (angle > 35 and angle <= 45):
        return (12, 83, 245)
    if (angle > 45 and angle <= 55):
        return (12, 245, 159)

    if (angle < -10 and angle >= -15):
        return (47, 245, 12)
    if (angle < -15 and angle >= -25):
        return (187, 245, 12)
    if (angle < -25 and angle >= -35):
        return (245, 173, 12)
    if (angle < -35 and angle >= -45):
        return (245, 4, 12)
    if (angle < -45 and angle >= -55):
        return (51, 51, 51)
    #default
    return (255, 255, 255)

cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw/encoded/1459324456.h264.mp4")
while True:
    if cap.grab():
        flag, frame = cap.retrieve()
        frame = frame[100:300, 0:800]
        frame = cv2.flip(frame, -1)
        frame = cv2.flip(frame, 1)
        edges = cv2.Canny(frame, 100, 200)

        font = cv2.FONT_HERSHEY_SIMPLEX

        sigma = 0.33
        v = np.median(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)
        # edges = cv2.Canny(image,100,200)


        lines = cv2.HoughLinesP(edged, 1, math.pi / 180, 80, 60, 1);

        for line in lines:

            dy = line[0][3] - line[0][1];
            dx = line[0][2] - line[0][0];
            angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

            # if (((angle < -31 and angle > -34) or (angle > 31 and angle < 35)) == False):
            #     continue

            if ((angle>-10 and angle <10) or (angle>-30 and angle <0) or (angle<30 and angle >0)):
                continue

            if (angle > 60 and angle <= 90):
                cv2.putText(frame, 'right swing', (500, 100), font, 1, (51, 51, 51), 1, cv2.LINE_AA)
                os.system('mpg321 /Users/saoron/cardiganCam/beep.mp3 &')
            if (angle < -60 and angle >= -90):
                cv2.putText(frame, 'left swing', (100, 100), font, 1, (51, 51, 51), 1, cv2.LINE_AA)
                os.system('mpg321 /Users/saoron/cardiganCam/beep.mp3 &')


            pt1 = (line[0][0], line[0][1])
            pt2 = (line[0][2], line[0][3])
            cv2.line(frame, pt1, pt2, getColorByAngle(angle), 2)



            cv2.putText(frame, str(angle), (line[0][0], line[0][1]), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow('video', edges)
        cv2.imshow('video1', frame)

    if cv2.waitKey(10) == 27:
        break