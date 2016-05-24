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

		# if the video should be flipped
		if self.config['flip'] == True:
			frame = cv2.flip(frame, -1)
			frame = cv2.flip(frame, 1)

		# get GPS data
		heading = open('./modules/gps/gps.json', 'r').read()
		# print '-------' + str(heading)

		# calibrate if needed
		if self.config['need_to_calibrate'] == True:
			self.calibration.calibrate(frame)
			self.config['need_to_calibrate'] = False


		# reload config
		self.config = Config().getConfig()

		roadFrame = frame.copy()
		cleanFrame = frame.copy()


		roadFrame = roadFrame[self.config['y1']:self.config['y1'] + self.config['road_height'], self.config['x1']:self.config['x1'] + self.config['road_width']]

		ldw = laneDepartureWarning(roadFrame, self.config['lane_center'], raspberry, cleanFrame)
		laneCenter = ldw.find_lanes(video)

		# draw which lane rect
		cv2.rectangle(cleanFrame, (0, 0), (100, 60), (255, 255, 255), -1);
		cv2.putText(cleanFrame, ldw.get_lane(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)
		cv2.putText(cleanFrame, str(heading), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)

		laneCenter += self.config['x1']

		leftCornerX = laneCenter - (self.config['square_width'] / 2)
		leftCornerY = 50

		x1 = int(laneCenter - (self.config['square_width'] / 2))
		y1 = (self.config['road_height']/2) + self.config['y1'] - self.config['square_height']
		x2 = laneCenter + (self.config['square_width'] / 2)
		y2 = (self.config['road_height']/2) + self.config['y1']

		# x1 = int(laneCenter - (width / 2))
		# y1 = 190
		# x2 = laneCenter + (width / 2)
		# y2 = 280


		laneCenter = forwardCollisionWarning(cleanFrame, x1, y1, x2, y2, raspberry, cleanFrame)



















