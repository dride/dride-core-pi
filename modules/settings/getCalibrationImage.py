########################################
#
# Return img with current calibration mode
#
########################################
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import cv2
from main.classes import frameAnalyzer
import time
from main.classes.capture import capture
from main.classes.PiVideoStream import PiVideoStream
from main.config import *



# initialize the camera and grab a reference to the raw camera capture
camera = PiVideoStream().start()
# allow the camera to warm up
time.sleep(2.0)

cap = capture(640, 480)
# reload config
config = Config().getConfig()


if cap.grab():
    flag, frame = cap.retrieve()

    roadFrame = frame[config['y1']:config['y1'] + config['road_height'],
	            config['x1']:config['x1'] + config['road_width']]

    # save thumbnail
    cv2.imwrite(PARENT_DIR + "thumb/last.jpg", frame)



# ldw = laneDepartureWarning(roadFrame, self.config['lane_center'], raspberry, cleanFrame)