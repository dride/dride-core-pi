import cv2
from classes import frameAnalyzer
import time
from classes.capture import capture
from classes.PiVideoStream import PiVideoStream
import json
from classes.gps import GPS
from config import *
from classes.sound import sound

def run_program():
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiVideoStream().start()
	
	# initialize the sound object
	soundObj = sound()

	# allow the camera to warm up
	time.sleep(2.0)

	# welcome message
	soundObj.raspberry = True
	soundObj.play_sound('hello', False)

	cap = capture(640, 480)

	# run cardigan processes
	try:
		while True:

			# reload config
			config = Config().getConfig()

			# load frame from camera
			frame = camera.read()

			# start record
			if config['dvr']:
				cap.captureFrame(frame)


			# get speed from GPS
			if config['gps']:
				position = json.loads(GPS.getPos())

			if (config['adas'] and (config['gps'] and position['speed'] > config['activation_speed'])) or config['in_calibration']:
				# Start ADAS process
				frameAnalyzer.analyze_frame(frame, True, True, True)


	except KeyboardInterrupt:
		print "\nattempting to close."
		camera.stop()
		print "\nBye Bye ;-)"

	camera.stop();


if __name__ == '__main__':
	run_program()
