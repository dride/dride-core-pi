# import the necessary packages
import numpy as np
import cv2
import math
import os
from matplotlib import pyplot as plt



from matplotlib import pyplot as plt


# load the image
img = cv2.imread('/Users/saoron/cardiganCam/training/set3/frame3820.jpg')


gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
threshhold, threshhold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
edges = cv2.Canny(threshhold_img, 150, 200, 3, 5)
lines = cv2.HoughLinesP(edges,1,np.pi/180,500, minLineLength = 600, maxLineGap = 75)[0].tolist()

for x1,y1,x2,y2 in lines:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)


cv2.imshow('img',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
