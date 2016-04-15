import numpy as np
import cv2
import math
import os
from classes.forwardCollisionWarning import forwardCollisionWarning


from classes.laneDepartureWarning import laneDepartureWarning





def analyze_frame(frame, flip, video):
	# forwardCollisionWarning(frame, 230, 210, 280, 320)
	laneDepartureWarning(frame, flip, video)

	# thread = Thread(target=find_lanes, args=(frame, flip, video))
	# thread.start()
	# thread.join()
















