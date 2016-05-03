import cv2
import numpy as np
from time import gmtime, strftime
import time
import picamera
from time import sleep
import os
from os import listdir
from os.path import isfile, join
import json

class capture:

	rolloverMinutes = 1
	rollover = rolloverMinutes * 60

	shutdownRequest = False

	def __init__(self, frame, x1, y1, x2, y2, raspberry):
		camera = picamera.PiCamera()
		camera.hflip = True
		while True:
			timestamp = int(round(time.time()))
			lastRollover = timestamp
			filename = str(timestamp)

			#save thumbnail
			camera.capture("/var/www/cardigan/thumbnail/" + filename + ".jpg", resize=(70, 70))
			camera.start_recording("/var/www/cardigan/video/" + filename + ".h264")
			sleep(60)
			camera.stop_recording()
			# decode to mp4
			os.system ("MP4Box -add /var/www/cardigan/video/"+filename+".h264 /var/www/cardigan/video/"+filename+".mp4; rm /var/www/cardigan/video/"+filename+".h264 &")

			# add file to index.json
			jsonRaw = ''
			path = "/var/www/cardigan/video/"
			files = [f for f in listdir(path) if isfile(join(path, f))]
			c = 0
			for file in files:
				files[c] = file.replace('.mp4', '')
				c+=1

			target = open("/var/www/cardigan/index.json", 'w')

			jsonRaw = json.dumps(files, default=lambda o: o.__dict__)
			target.write(jsonRaw)


			if(timestamp != lastRollover and (timestamp % self.rollover) == 0):
				lastRollover = timestamp
				break
			timestamp = int(round(time.time()))

		camera.release()



