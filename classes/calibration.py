import cv2
import numpy as np


class calibration:

	frame = None

	def __init__(self, frame):

		self.frame = frame

	def calibrate(self):

		self.frame = self.frame[200:320, 200:500]