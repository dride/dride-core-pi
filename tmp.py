# import the necessary packages
import numpy as np
import cv2
import math
import os
from linear import Point
from matplotlib import pyplot as plt



from matplotlib import pyplot as plt


# load the image
image = cv2.imread('/Users/saoron/Desktop/untitled folder 2/road/frame830.jpg')
# image = image[100:250, 0:500]
# image = cv2.flip(image, -1)
# image = cv2.flip(image, 1)
edges = cv2.Canny(image, 100, 200)

font = cv2.FONT_HERSHEY_SIMPLEX

sigma = 0.33
v = np.median(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# apply automatic Canny edge detection using the computed median
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
edged = cv2.Canny(blurred, lower, upper)


lines = cv2.HoughLinesP(edged, 1, math.pi / 180, 80, 1, 20);
print lines
linesWithLabel = [[], [], [], [], [], [], [], [], [], [], []]
linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], []]

if (lines is not None) :
    for line in lines:

        dy = line[0][3] - line[0][1];
        dx = line[0][2] - line[0][0];
        angle = int(math.atan2(dy, dx) * 180.0 / math.pi);
        print angle
        #
        # if (((angle < -30 and angle >= -45) or (angle > 30 and angle <= 45)) == False):
        #     continue
        #
        #
        # if (angle>-10 and angle <10):
        #     continue

        if (angle > 60 and angle <= 90):
            cv2.putText(image, 'right swing', (500, 100), font, 1, (51, 51, 51), 1, cv2.LINE_AA)

        if (angle < -60 and angle >= -90):
            cv2.putText(image, 'left swing', (100, 100), font, 1, (51, 51, 51), 1, cv2.LINE_AA)


        avgX = (line[0][0] + line[0][2]) / 2
        avgY = (line[0][1] + line[0][3]) / 2

        # if (avgX <=150):
        #     print 'DETECT IF THE COLOR IS ~WHITE' + frame[avgX][avgY]

        cv2.circle(image, (avgX, avgY), 5, getColorByAngle(angle), -1)

        linesWithLabel[int(getGroupIdByAngle(angle))].append([avgX, avgY])
        linesWithLabelColor[int(getGroupIdByAngle(angle))].append(getColorByAngle(angle))

        pt1 = (line[0][0], line[0][1])
        pt2 = (line[0][2], line[0][3])
        cv2.line(image, pt1, pt2, getColorByAngle(angle), 2)




print linesWithLabel

# show the images
cv2.imshow("images",edged)
cv2.imshow("images2", np.hstack([image]))
cv2.waitKey(0)
