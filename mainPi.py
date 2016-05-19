import cv2
from classes import frameAnalyzer
import time
from classes.capture import capture
from classes.PiVideoStream import PiVideoStream
from threading import Thread

def capture(camera):
	# start record
	cap = capture(camera.camera)
	cap.captureClips()



def run_program():
	# load the image
	# image = cv2.imread('/Users/saoron/cardiganCam/training/set6/3.png')
	# frameAnalyzer.analyze_frame(image, True, False)
	#

	# initialize the camera and grab a reference to the raw camera capture
	camera = PiVideoStream().start()
	# allow the camera to warmup
	time.sleep(2.0)



	# run cardigan proccesses
	try:
		while True:
			Thread(target=capture(camera), args=()).start()


			# Start safty proccess
			frame = camera.read()
			frameAnalyzer.analyze_frame(frame, True, True, True)


	except KeyboardInterrupt:
		print "\nattempting to close."
		camera.stop()
		print "\nBye Bye ;-)"



	camera.stop();

if __name__ == '__main__':
	run_program()