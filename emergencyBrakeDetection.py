# import the necessary packages
import numpy as np
import argparse
import cv2
import os
from classes import frameAnalyzer
import math
from classes.frameMemory import frameMemory


def color_variant(hex_color, brightness_offset=1):
	""" takes a color like #87c95f and produces a lighter or darker variant """
	if len(hex_color) != 7:
		raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
	rgb_hex = [hex_color[x:x + 2] for x in [1, 3, 5]]
	new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
	new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]  # make sure new values are between 0 and 255
	return new_rgb_int



cap = cv2.VideoCapture("/Users/saoron/Desktop/driveRaw4/encoded/1459726144.h264.mp4")


font = cv2.FONT_HERSHEY_SIMPLEX

boundaries = [
	(color_variant('#5F5125', -50), color_variant('#5F5125', 50))
]
isCarArray = frameMemory(5)
frameNumber = 0
while True:
	if cap.grab():
		frameNumber+=1
		flag, frame = cap.retrieve()

		x1 = 230
		y1 = 210
		x2 = 280
		y2 = 320

		frame = cv2.flip(frame, -1)
		frame = cv2.flip(frame, 1)
		cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

		image = np.zeros((160, 90, 3), np.uint8)
		image[:] = (255, 255, 255)

		#
		frame2 = frame
		frame = frame[y1:y2, x1:x2]

		sigma = 0.33
		v = np.median(frame)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# apply automatic Canny edge detection using the computed median
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(frame, lower, upper)

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		corners = cv2.goodFeaturesToTrack(edged, 500, 0.4, 10)
		if corners is not None:
			corners = np.int0(corners)

			cornerCount = 0
			for i in corners:
				x, y = i.ravel()

				if 0 <= x <= 1 or 0 <= y <= 1 or x1-1 <= x <= x1+1 or y1+1 <= y <= y1+1:
					continue
				else:
					cornerCount += 1
					cv2.circle(frame, (x, y), 3, 255, -1)

			if cornerCount > 9:
				print cornerCount
				cv2.putText(frame2, "CAR AHEAD", (50, 50), font, 2, (51, 51, 51), 6, cv2.LINE_AA)


	# cv2.imshow('video2', edged)
	cv2.imshow('video4', image)
	cv2.imshow('video1', edged)
	cv2.imshow('video2', frame2)

	if cv2.waitKey(10) == 27:
		break

