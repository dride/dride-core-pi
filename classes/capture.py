import cv2
import numpy as np
from time import gmtime, strftime
import time
import picamera
import sys
from time import sleep
import os
from config import *


class capture:

	rolloverMinutes = 1
	rollover = rolloverMinutes * 60
	camera  = None
	shutdownRequest = False
	parent = PARENT_DIR + '/modules/video/'

	def __init__(self, camera):

		self.camera = camera
		self.camera.hflip = True


	def captureClips(self):

		while True:
			timestamp = int(round(time.time()))
			lastRollover = timestamp
			filename = str(timestamp)

			#save thumbnail
			self.camera.capture(self.parent + "thumb/" + filename + ".jpg", resize=(70, 70))
			self.camera.start_recording(self.parent + "clip/" + filename + ".h264")
			# save GPS data for frame
			file = open(self.parent + "gps/" + filename + ".json", 'w')


			sleep(60)
			self.camera.stop_recording()
			# decode to mp4
			os.system ("MP4Box -add " + self.parent + "clip/"+filename+".h264 " + self.parent+"clip/" + filename+".mp4; rm "+self.parent + "clip/" + filename+".h264 &")



			if(timestamp != lastRollover and (timestamp % self.rollover) == 0):
				lastRollover = timestamp
				break
			timestamp = int(round(time.time()))

		self.camera.release()

