########################################
#
# Return img with current calibration mode
#
########################################

import cv2
from classes import frameAnalyzer
import time
from classes.capture import capture
from classes.PiVideoStream import PiVideoStream
from config import *



# initialize the camera and grab a reference to the raw camera capture
camera = PiVideoStream().start()
# allow the camera to warm up
time.sleep(2.0)

cap = capture(640, 480)
# reload config
config = Config().getConfig()


if cap.grab():
        flag, frame = cap.retrieve()

        # start record
        capture.captureFrame(frame)
roadFrame = frame[config['y1']:config['y1'] + config['road_height'],
            config['x1']:config['x1'] + config['road_width']]
cv2.imshow('img322323231', frame)

# ldw = laneDepartureWarning(roadFrame, self.config['lane_center'], raspberry, cleanFrame)