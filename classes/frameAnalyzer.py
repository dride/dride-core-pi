import numpy as np
import cv2
import math
import os
from classes.forwardCollisionWarning import forwardCollisionWarning



from classes.laneDepartureWarning import laneDepartureWarning




def analyze_frame(frame, flip, video, raspberry = False):

	# get GPS data
	heading = open('./modules/gps/gps.json', 'r').read()
	print '-------' + str(heading)
	cleanFrame = frame.copy()

	laneCenter = 100
	y1 = 350 # 4.5.16 ->200
	x1 = 200
	roadFrame = frame.copy()
	# uncomment if needed to flip
	# roadFrame = cv2.flip(roadFrame, -1)
	# roadFrame = cv2.flip(roadFrame, 1)

	roadFrame = roadFrame[y1:y1 + 120, x1:x1 + 300]

	ldw = laneDepartureWarning(roadFrame, flip, video, laneCenter, raspberry)
	laneCenter = ldw.find_lanes(flip, video)

	# draw which lane rect
	cv2.rectangle(cleanFrame, (0, 0), (100, 60), (255, 255, 255), -1);
	cv2.putText(cleanFrame, ldw.get_lane(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)
	cv2.putText(cleanFrame, str(heading), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)


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


	laneCenter = forwardCollisionWarning(cleanFrame, x1, y1, x2, y2, raspberry)



















