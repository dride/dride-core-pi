import cv2
import numpy as np


class LaneDetection(object):

	def __init__(self, frame):
		self.frame = frame

	# predict what lane are we in
	def predict_lane(self, lines, debug=True):
		right = 0
		left = 0
		lane = ''
		for line in lines:

			if self.get_lane_direction_by_point(line):
				left += 1
			else:
				right += 1
		if debug:
			cv2.rectangle(self.frame, (0, 0), (100, 30), (255, 255, 255), -1);

			if left > right:
				lane = "Left Lane"
			else:
				lane = "Right Lane"

			cv2.putText(self.frame, lane, (10, 20), self.font, 0.5, (51, 51, 51), 1, cv2.LINE_AA)

		return left > right


	# Return True if point is in Left lane
	def get_lane_direction_by_point(self, line):
		right = 0
		left = 0

		avgX = (line[0][0] + line[0][2]) / 2

		if avgX > self.width / 2:
			right += 1
		else:
			left += 1

		return left > right