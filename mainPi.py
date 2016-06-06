import cv2
from classes import frameAnalyzer
import time
from classes.capture import capture
from classes.PiVideoStream import PiVideoStream
import json
from classes.gps import GPS
from config import *

def run_program():

	# initialize the camera and grab a reference to the raw camera capture
	camera = PiVideoStream().start()
	# allow the camera to warm up
	time.sleep(2.0)

	cap = capture(640, 480)
	# reload config
	config = Config().getConfig()

	# run cardigan proccesses
	try:
		while True:
			# load frame from camera
			frame = camera.read()

			# start record
			cap.captureFrame(frame)


			# get GPS data
			position = json.loads(GPS.getPos())
			if position and position['speed'] < config['activation_speed']:
				# Start ADAS process
				frameAnalyzer.analyze_frame(frame, True, True, True)


	except KeyboardInterrupt:
		print "\nattempting to close."
		camera.stop()
		print "\nBye Bye ;-)"



	camera.stop();

if __name__ == '__main__':
	run_program()