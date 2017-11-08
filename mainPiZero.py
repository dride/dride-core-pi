import time
import picamera
import json
from classes.gps import GPS
from config import *
import datetime  # new
import sys, os


def run_program():
	# initialize the camera and grab a reference to the raw camera capture
	camera = picamera.PiCamera()
	camera.resolution = (1280, 720)

	# allow the camera to warm up
	time.sleep(2.0)

	def get_file_name():
		return str(int(round(time.time())))

	parent = PARENT_DIR + '/modules/video/'

	# run cardigan processes
	try:

		while True:

			# reload config
			config = Config().getConfig()
			fileName = get_file_name()
			## save thumb
			camera.resolution = (400, 225)
			camera.capture(parent + "thumb/" + fileName + ".jpg")
			camera.resolution = (1280, 720)
			# start record
			if config['dvr'] :
				camera.start_recording(parent + "clip/" + fileName + ".h264")

			camera.wait_recording(60)
			camera.stop_recording()
			os.system('MP4Box -add '+parent + "clip/" + fileName + ".h264 " + parent + "clip/" + fileName + ".mp4")
			os.remove(parent + "clip/" + fileName + ".h264")



	except KeyboardInterrupt:
		print "\nattempting to close."
		camera.stop_recording()
		print "\nBye Bye ;-)"


if __name__ == '__main__':
	run_program()
