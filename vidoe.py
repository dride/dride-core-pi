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
cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw/encoded/1459324636.h264.mp4")
c=0
while True:
    if cap.grab():
        flag, frame = cap.retrieve()
        c += 1
        print c

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


        lines = cv2.HoughLinesP(edged, 1, math.pi / 180, 80, 60, 20);
        linesWithLabel = [[], [], [], [], [], [], [], [], [], [], []]
        linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], []]
        if (lines is not None) :
            for line in lines:

                dy = line[0][3] - line[0][1];
                dx = line[0][2] - line[0][0];
                angle = int(math.atan2(dy, dx) * 180.0 / math.pi);
                #
                # if (((angle < -30 and angle >= -45) or (angle > 30 and angle <= 45)) == False):
                #     continue
                #
                #
                if (angle>-10 and angle <10):
                    continue

                if (angle > 60 and angle <= 90):
                    cv2.putText(frame, 'right swing', (500, 100), font, 1, (51, 51, 51), 1, cv2.LINE_AA)
                    os.system('mpg321 /Users/saoron/cardiganCam/beep.mp3 &')
                if (angle < -60 and angle >= -90):
                    cv2.putText(frame, 'left swing', (100, 100), font, 1, (51, 51, 51), 1, cv2.LINE_AA)
                    os.system('mpg321 /Users/saoron/cardiganCam/beep.mp3 &')

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

        # for index in range(len(linesWithLabel)):
        #     if (len(linesWithLabel[index]) < 2):
        #         linesWithLabel[index] = []
        #     else:
        #         Z = np.float32(linesWithLabel[index])
        #
        #         # define criteria and apply kmeans()
        #         criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        #         ret, label, center = cv2.kmeans(Z, 2, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        #
        #         # Now separate the data, Note the flatten()
        #         A = Z[label.ravel() == 0]
        #         B = Z[label.ravel() == 1]
        #
        #         for i in range(len(center)):
        #             cv2.circle(frame, (center[0][0], center[0][1]), 6, (255, 0, 255), -1)
        #             # cv2.line(frame, (center[i][0], center[i][1]),
        #             #          (center[i][0], center[i][0]),
        #             #          (255,255,255),
        #             #          2
        #             #          )


        cv2.imshow('video', edges)
        cv2.imshow('video1', frame)


    if cv2.waitKey(10) == 27:
        break