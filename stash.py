# import the necessary packages
import numpy as np
import cv2
import math

from matplotlib import pyplot as plt

def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    return new_rgb_int



# load the image
image = cv2.imread('/Users/saoron/cardiganCam/data/2.png')
sigma=0.33
v = np.median(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

# apply automatic Canny edge detection using the computed median
lower = int(max(0, (1.0 - sigma) * v))
upper = int(min(255, (1.0 + sigma) * v))
edged = cv2.Canny(blurred, lower, upper)
# edges = cv2.Canny(image,100,200)


lines = cv2.HoughLinesP(edged, 1, 0.07, 80, 30, 1);

for line in lines:
    print line[0]
    pt1 = (line[0][0],line[0][1])
    pt2 = (line[0][2],line[0][3])
    cv2.line(image, pt1, pt2, (0,0,0), 3)



# show the images
cv2.imshow("images", np.hstack([image]))
cv2.waitKey(0)
