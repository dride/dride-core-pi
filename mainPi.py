import cv2
from classes import frameAnalyzer
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from classes.capture import capture
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera

# load the image
# image = cv2.imread('/Users/saoron/cardiganCam/training/set6/3.png')
# frameAnalyzer.analyze_frame(image, True, False)
#

# initialize the camera and grab a reference to the raw camera capture
camera = PiVideoStream().start()
# allow the camera to warmup
time.sleep(2.0)


# start record
cap = capture(camera)
cap.captureClips()

# run cardigan proccesses
while True:
	frame = camera.read()
	frameAnalyzer.analyze_frame(frame, True, True, True)


camera.stop();