import cv2
from classes import frameAnalyzer
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


# load the image
# image = cv2.imread('/Users/saoron/cardiganCam/training/set6/3.png')
# frameAnalyzer.analyze_frame(image, True, False)
#

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

for framePi in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if True:
        frame = framePi.array

        frameAnalyzer.analyze_frame(frame, True, True, True)
    rawCapture.truncate(0)
