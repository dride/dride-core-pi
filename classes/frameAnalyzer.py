import cv2
from config import *
from classes.forwardCollisionWarning import forwardCollisionWarning
from classes.calibration import calibration
from classes.gps import GPS
from classes.laneDepartureWarning import laneDepartureWarning
import json

class analyze_frame:

	# load config
	config = Config().getConfig()
	laneAvg = -1
	# load calibration object
	calibration = calibration()

	def __init__(self, frame, flip, video, raspberry = False):


		# if the video should be flipped
		if self.config['flip'] == True:
			frame = cv2.flip(frame, -1)
			frame = cv2.flip(frame, 1)

		# get GPS data
		position = json.loads(GPS.getPos())


		if position and position['speed'] < self.config['activation_speed']:
			return

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
		if position:
			cv2.putText(cleanFrame, ldw.get_lane(), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)
			cv2.putText(cleanFrame, 'Heading: ' + str(position['heading']), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)
			cv2.putText(cleanFrame, 'Speed: ' +str(position['speed']), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)
			cv2.putText(cleanFrame, 'Point: (' + str(position['latitude']) + ',' + str(position['longitude']) + ')', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (51, 51, 51), 1, cv2.LINE_AA)

		laneCenter += self.config['x1']
		self.laneAvg = ldw.get_lane_avg_x()

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



















