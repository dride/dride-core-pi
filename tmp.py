import cv2
import numpy as np
import math


cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw6/1461661168.mp4")
while True:
    # if c >0:
    #     cv2.waitKey(0)
    # c +=1
    # # print c
    if cap.grab():
        flag, frame = cap.retrieve()
        image = frame
        # image = cv2.flip(image, -1)
        # image = cv2.flip(image, 1)

        font = cv2.FONT_HERSHEY_SIMPLEX

        sigma = 0.33
        v = np.median(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(gray, lower, upper)

        lines = cv2.HoughLinesP(edged, 1, math.pi / 360, 6, 30, 6);

        if (lines is not None):
            for line in lines:


                dy = line[0][3] - line[0][1];
                dx = line[0][2] - line[0][0];
                angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

                if (angle != 0 ):
                    continue


                pt1 = (line[0][0], line[0][1])
                pt2 = (line[0][2], line[0][3])

                cv2.line(image, pt1, pt2, (255,255,0), 2)
                cv2.putText(image, str(angle), (line[0][0] + 20, line[0][1]), font, 0.6, (51, 51, 51), 1, cv2.LINE_AA)

    cv2.imshow('img1', image)
    cv2.waitKey(0)