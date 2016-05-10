import cv2
import numpy as np
from config import *


class calibration:

	frame = None
	# load config
	config = Config()


	def __init__(self):

		self.frame = None

	def needToCalibrate(self):

		return True

	def calibrate(self, frame):
		# probably a set of frames !!!
		self.frame = frame

		# self.frame = self.frame[200:320, 200:500]
		Y1 = 0  # 4.5.16 ->200
		X1 = 0

		# print self.config.res['x1']
		#
		# self.config.updateConfigNode('calibration', 'x1', '100')
		#
		# print self.config.res['x1']