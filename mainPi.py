import cv2
from classes import frameAnalyzer
import time
from classes.capture import capture
from classes.PiVideoStream import PiVideoStream
import json
from classes.gps import GPS
from config import *
from classes.sound import sound

from modules.indicators.python.states.indicators import Indicators

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
	# welcome light
	indicator = Indicators()
	indicator.wakeWord()



	# reload config
	config = Config().getConfig()

	cap = capture(1024, 768, config)

	frameNumber = 0

	# run cardigan processes
	try:
		while True:

			# reload config
			config = Config().getConfig()

			# load frame from camera
			frame = camera.read()
			frameNumber +=1
			
			# rotate 90 deg
			frame = capture.rotate_image(frame, 90)

			# start record
			if config['dvr'] and not config['in_calibration']:
				cap.captureFrame(frame)


			# get speed from GPS
			if config['gps']:
				position = json.loads(GPS.getPos())

			if (config['adas'] and (config['gps'] and float(position['speed']) > float(config['activation_speed']))) or config['in_calibration']:
				# Start ADAS process
				frameAnalyzer.analyze_frame(frame, True, True, True, frameNumber)


	except KeyboardInterrupt:
		print "\nattempting to close."
		camera.stop()
		print "\nBye Bye ;-)"

	camera.stop();


if __name__ == '__main__':
	run_program()
