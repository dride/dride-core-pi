import cv2
import time
from config import *
from classes.gps import GPS


class capture:

	# load config
	config = Config().getConfig()

	rolloverMinutes = 1
	rollover = rolloverMinutes * 60
	camera  = None
	shutdownRequest = False
	parent = PARENT_DIR + '/modules/video/'
	out = None
	# Define the codec
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	timestamp = int(round(time.time()))
	lastRollover = 0
	gps = GPS()
	filename = '';

	def __init__(self, w, h):

		self.w = w
		self.h = h

	def captureFrame(self, frame):

		# if we dont have any video object or we need to replace file due to size limit
		if self.out is None or (self.timestamp != self.lastRollover and (self.timestamp % self.rollover) == 0):

			# Release everything if job is finished
			if self.out is not None:
				self.out.release()

			# save current timestamp
			self.timestamp = int(round(time.time()))
			self.lastRollover = self.timestamp
			self.lastRollover = self.timestamp

			self.filename = str(self.timestamp)

			# save thumbnail
			cv2.imwrite(self.parent + "thumb/" + self.filename + ".jpg", frame)

			# create GPS file
			if self.config['gps'] == True:
				self.gps.createNewGPSrecordFile(self.filename)

			# Create new VideoWriter object
			self.out = cv2.VideoWriter(self.parent + "clip/" + self.filename + ".avi", self.fourcc, 20.0, (self.w, self.h))


		if self.config['gps']==True:
			# save GPS data for frame
			self.gps.AppendGPSPositionToCurrentFile(self.filename)

		# write the frame to video file
		self.out.write(frame)

		self.timestamp = int(round(time.time()))


