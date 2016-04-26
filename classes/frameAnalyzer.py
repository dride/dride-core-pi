import numpy as np
import cv2
import math
import os
from classes.forwardCollisionWarning import forwardCollisionWarning


from classes.laneDepartureWarning import laneDepartureWarning




def analyze_frame(frame, flip, video):

	laneCenter = 250
	ldw = laneDepartureWarning(frame, flip, video, laneCenter)
	laneCenter = ldw.find_lanes(flip, video)

	width = 50
	leftCornerX = laneCenter - (width / 2)
	leftCornerY = 50

	x1 = int(laneCenter - (width / 2))
	y1 = 230
	x2 = laneCenter + (width / 2)
	y2 = 280

	# x1 = int(laneCenter - (width / 2))
	# y1 = 190
	# x2 = laneCenter + (width / 2)
	# y2 = 280


	laneCenter = forwardCollisionWarning(frame, x1, y1, x2, y2)



















