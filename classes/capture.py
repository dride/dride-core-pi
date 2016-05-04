import cv2
import numpy as np
from time import gmtime, strftime
import time
import picamera
from time import sleep
import os

class capture:

	rolloverMinutes = 1
	rollover = rolloverMinutes * 60

	shutdownRequest = False

	def __init__(self):
		camera = picamera.PiCamera()
		camera.hflip = True
		while True:
			timestamp = int(round(time.time()))
			lastRollover = timestamp
			filename = str(timestamp)

			#save thumbnail
			camera.capture("modules/video/thumb/" + filename + ".jpg", resize=(70, 70))
			camera.start_recording("modules/video/clip/" + filename + ".h264")
			sleep(60)
			camera.stop_recording()
			# decode to mp4
			os.system ("MP4Box -add modules/video/clip/"+filename+".h264 modules/video/clip/"+filename+".mp4; rm modules/video/clip/"+filename+".h264 &")



			if(timestamp != lastRollover and (timestamp % self.rollover) == 0):
				lastRollover = timestamp
				break
			timestamp = int(round(time.time()))

		camera.release()



