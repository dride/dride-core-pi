import numpy as np
import cv2
import math
import os
from classes.forwardCollisionWarning import forwardCollisionWarning


from classes.laneDepartureWarning import laneDepartureWarning




def analyze_frame(frame, flip, video):


	cleanFrame = frame.copy()

	laneCenter = 100
	ldw = laneDepartureWarning(frame, flip, video, laneCenter)
	laneCenter = ldw.find_lanes(flip, video)

	# draw which lane rect
	cv2.rectangle(cleanFrame, (0, 0), (100, 30), (255, 255, 255), -1);
	cv2.putText(cleanFrame, ldw.get_lane(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)


	deltaX = 200
	deltaY = 50

	laneCenter += deltaX

	width = 40
	leftCornerX = laneCenter - (width / 2)
	leftCornerY = 50

	x1 = int(laneCenter - (width / 2))
	y1 = 310 + deltaY
	x2 = laneCenter + (width / 2)
	y2 = 350 + deltaY

	# x1 = int(laneCenter - (width / 2))
	# y1 = 190
	# x2 = laneCenter + (width / 2)
	# y2 = 280


	laneCenter = forwardCollisionWarning(cleanFrame, x1, y1, x2, y2)



















