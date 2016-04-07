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
    return (0, 255, 255, 255)



def getGroupIdByAngle(angle):

    if (angle > 10 and angle <= 15):
        return 1
    if (angle > 15 and angle <= 25):
        return 2
    if (angle > 25 and angle <= 35):
        return 3
    if (angle > 35 and angle <= 45):
        return 4
    if (angle > 45 and angle <= 55):
        return 5

    if (angle < -10 and angle >= -15):
        return 6
    if (angle < -15 and angle >= -25):
        return 7
    if (angle < -25 and angle >= -35):
        return 8
    if (angle < -35 and angle >= -45):
        return 9
    if (angle < -45 and angle >= -55):
        return 10
    #default
    return 0


linesWithLabel = [[], [], [], [], [], [], [], [], [], [], []]
linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], []]
cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw4/encoded/1459726230.h264.mp4")
c=0
while True:
    if cap.grab():
        flag, frame = cap.retrieve()
        c += 1
        # print c

        frame = frame[100:250, 0:500]
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
        edged = cv2.Canny(frame, lower, upper)

        lines = cv2.HoughLinesP(edged, 1, math.pi / 360, 20, 30, 10);
        linesWithLabel = [[], [], [], [], [], [], [], [], [], [], []]
        linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], []]
        right = 0
        left = 0
        goodLines = 0
        if (lines is not None) :
            for line in lines:
                dy = line[0][3] - line[0][1];
                dx = line[0][2] - line[0][0];
                angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

                if (angle ==90 or angle == -90 or angle==0):
                    continue

                if (angle > 60 and angle <= 90):
                    right += 1
                if (angle < -60 and angle >= -90):
                    left += 1

                if (((angle < -30 and angle >= -45) or (angle > 30 and angle <= 45)) == False):
                    continue

                if (angle>-10 and angle <10):
                    continue

                # # experimenal - if too many line > 50 we can stop looking
                # # Migt be problamatic in case of departure
                goodLines += 1
                print goodLines
                # if (goodLines > 50):
                #     break

                avgX = (line[0][0] + line[0][2]) / 2
                avgY = (line[0][1] + line[0][3]) / 2

                # if (avgX <=150):
                #     print 'DETECT IF THE COLOR IS ~WHITE' + frame[avgX][avgY]

                cv2.circle(frame, (avgX, avgY), 5, getColorByAngle(angle), -1)

                linesWithLabel[int(getGroupIdByAngle(angle))].append([avgX, avgY])
                linesWithLabelColor[int(getGroupIdByAngle(angle))].append(getColorByAngle(angle))

                pt1 = (line[0][0], line[0][1])
                pt2 = (line[0][2], line[0][3])
                cv2.line(frame, pt1, pt2, getColorByAngle(angle), 2)
                # cv2.putText(frame, str(angle), (line[0][0], line[0][1]), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        print str(right) + '--' + str(left)
        if (right > 2):
            cv2.putText(frame, 'right swing', (500, 100), font, 2, (0, 0, 0), 1, cv2.LINE_AA)
            print angle
            os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/beep.mp3 &')
        if (left > 2):
            cv2.putText(frame, 'left swing', (100, 100), font, 2, (0, 0, 0), 1, cv2.LINE_AA)
            print angle
            os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/beep.mp3 &')

        cv2.imshow('video', edges)
        cv2.imshow('video1', frame)


    if cv2.waitKey(10) == 27:
        break