import numpy as np
import cv2
import math
import os
from config import *
from classes.forwardCollisionWarning import forwardCollisionWarning
from classes.calibration import calibration

from classes.laneDepartureWarning import laneDepartureWarning

class analyze_frame:

	# load config
	config = Config().getConfig()

	# load calibration object
	calibration = calibration()

	def __init__(self, frame, flip, video, raspberry = False):

		# get GPS data
		heading = open('./modules/gps/gps.json', 'r').read()
		print '-------' + str(heading)

		# calibrate if needed
		if self.calibration.needToCalibrate:
			self.calibration.calibrate(frame)
			# reload config
			self.config = Config().getConfig()

		cleanFrame = frame.copy()


		roadFrame = frame.copy()
		cleanFrame = frame.copy()
		# uncomment if needed to flip
		# roadFrame = cv2.flip(roadFrame, -1)
		# roadFrame = cv2.flip(roadFrame, 1)

		roadFrame = roadFrame[self.config['y1']:self.config['y1'] + self.config['road_height'], self.config['x1']:self.config['x1'] + self.config['road_width']]

		ldw = laneDepartureWarning(roadFrame, flip, video, self.config['lane_center'], raspberry, cleanFrame)
		laneCenter = ldw.find_lanes(flip, video)

		# draw which lane rect
		cv2.rectangle(cleanFrame, (0, 0), (100, 60), (255, 255, 255), -1);
		cv2.putText(cleanFrame, ldw.get_lane(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)
		cv2.putText(cleanFrame, str(heading), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)

		laneCenter += self.config['deltaX']

		leftCornerX = laneCenter - (self.config['square_width'] / 2)
		leftCornerY = 50

		x1 = int(laneCenter - (self.config['square_width'] / 2))
		y1 = 260 + self.config['deltaY']
		x2 = laneCenter + (self.config['square_width'] / 2)
		y2 = 300 + self.config['deltaY']

		# x1 = int(laneCenter - (width / 2))
		# y1 = 190
		# x2 = laneCenter + (width / 2)
		# y2 = 280


		laneCenter = forwardCollisionWarning(cleanFrame, x1, y1, x2, y2, raspberry, cleanFrame)



















