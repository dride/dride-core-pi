import cv2
import numpy as np
import time
from config import *
from classes.gps import GPS


class capture():

	# load config
	config = Config().getConfig()

	rolloverMinutes = 1
	rollover = rolloverMinutes * 60
	camera  = None
	shutdownRequest = False
	parent = PARENT_DIR + '/modules/video/'
	out = None
	# Define the codec
	# TODO : inject codec by OS
	fourcc = cv2.VideoWriter_fourcc(*'X264')
	timestamp = int(round(time.time()))
	lastRollover = 0
	gps = GPS()
	filename = ''

	def __init__(self, w, h):

		self.w = w
		self.h = h

	def captureFrame(self, frame):

		# if the video should be flipped
		if self.config['flip'] == True:
			frame = cv2.flip(frame, -1)
			frame = cv2.flip(frame, 1)
			
		# if we dont have any video object or we need to replace file due to size limit
		if self.out is None or (self.timestamp != self.lastRollover and (self.timestamp % self.rollover) == 0):

			# Release everything if job is finished
			if self.out is not None:
				self.out.release()

			# save current timestamp
			self.timestamp = self.get_time()
			self.lastRollover = self.timestamp
			self.lastRollover = self.timestamp

			self.filename = str(self.timestamp)

			# save thumbnail
			cv2.imwrite(self.parent + "thumb/" + self.filename + ".jpg", frame)

			# create GPS file
			if self.config['gps'] == True:
				self.gps.createNewGPSrecordFile(self.filename)

			# Create new VideoWriter object
			self.out = cv2.VideoWriter(self.parent + "clip/" + self.filename + ".mp4", self.fourcc, FPS, (self.w, self.h))


		if self.config['gps']==True:
			# save GPS data for frame
			self.gps.AppendGPSPositionToCurrentFile(self.filename)

		# add waterMark
		# read images
		mark = cv2.imread(PARENT_DIR + '/assets/images/watermark.png')
		m, n = frame.shape[:2]
		# create overlay image with mark at the upper left corner, use uint16 to hold sum
		overlay = np.zeros_like(frame, "uint16")
		overlay[:mark.shape[0], :mark.shape[1]] = mark
		# add the images and clip (to avoid uint8 wrapping)
		frame = np.array(np.clip(frame + overlay, 0, 255), "uint8")

		# write the frame to video file
		self.out.write(frame)

		self.timestamp = self.get_time()

	# return time form file or take from device
	# The biggest problem is that the device don't have internet connection
	# and because of that the time is incorrect!
	@classmethod
	def get_time(self):

		file = open(PARENT_DIR + "/modules/gps/time.json", 'r')
		timeByFile = file.read()

		return int(round(time.time()))
		# return timeByFile if timeByFile != '' else int(round(time.time()))
