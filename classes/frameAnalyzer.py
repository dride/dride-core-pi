import numpy as np
import cv2
import math
import os



def color_variant(hex_color, brightness_offset=1):
	""" takes a color like #87c95f and produces a lighter or darker variant """
	if len(hex_color) != 7:
		raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
	rgb_hex = [hex_color[x:x + 2] for x in [1, 3, 5]]
	new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
	new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]  # make sure new values are between 0 and 255
	return new_rgb_int

def get_color_by_angle(angle):

	if 10 < angle <= 15:
		return 245, 12, 12
	if 15 < angle <= 25:
		return 245, 12, 184
	if 25 < angle <= 35:
		return 134, 12, 245
	if 35 < angle <= 45:
		return 12, 83, 245
	if 45 < angle <= 55:
		return 12, 245, 159

	if -15 < angle >= -10:
		return 47, 245, 12
	if -10 < angle >= -15:
		return 187, 245, 12
	if -15 < angle >= -25:
		return 245, 173, 12
	if -25 < angle >= -35:
		return 245, 4, 12
	if -35 < angle >= -45:
		return 51, 51, 51
	if -45 < angle >= -55:
		return 12, 65, 19

	# default color
	return 0, 255, 255

def get_group_id_by_angle(angle):

	if 10 < angle <= 15:
		return 1
	if 15 < angle <= 25:
		return 2
	if 25 < angle <= 35:
		return 3
	if 35 < angle <= 45:
		return 4
	if 45 < angle <= 55:
		return 5

	if -15 > angle >= -10:
		return 6
	if -10 > angle >= -15:
		return 7
	if -15 > angle >= -25:
		return 8
	if -25 > angle >= -35:
		return 9
	if -35 > angle >= -45:
		return 10
	if -45 > angle >= -55:
		return 11

	# default group
	return 0


def show_frame(frame1, frame2, video):

	cv2.imshow('img1', frame1)
	cv2.imshow('img2', frame2)

	if video:
		cv2.waitKey(27)
	else:
		cv2.waitKey(0)


def analyze_frame(frame, flip, video):
	find_lanes(frame, flip, video)


# Find lanes using angle
def find_lanes(frame, flip, video):
	linesWithLabel = [[], [], [], [], [], [], [], [], [], [], [], []]
	linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], [], []]

	if flip:
		frame = frame[100:240, 0:500]
		# frame = frame[0:250, 200:500]
		frame = cv2.flip(frame, -1)
		frame = cv2.flip(frame, 1)

	edges = cv2.Canny(frame, 100, 200)
	font = cv2.FONT_HERSHEY_SIMPLEX
	sigma = 0.33
	v = np.median(frame)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(gray, lower, upper)

	lines = cv2.HoughLinesP(edged, 1, math.pi / 360, 10, 30, 9);
	linesWithLabel = [[], [], [], [], [], [], [], [], [], [], [], []]
	linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], [], []]
	right = 0
	left = 0
	goodLines = 0
	if (lines is not None) :
		for line in lines:

			dy = line[0][3] - line[0][1];
			dx = line[0][2] - line[0][0];
			angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

			if (angle == 90 or angle == -90 or angle == 0):
				continue

			if (angle > 60 and angle <= 90):
				right += 1
			if (angle < -60 and angle >= -90):
				left += 1

			if (((angle < -30 and angle >= -45) or (angle > 30 and angle <= 45)) == False):
				continue

			if (angle > -10 and angle < 10):
				continue

			# # experimenal - if too many line > 50 we can stop looking
			# # Migt be problamatic in case of departure
			# goodLines += 1
			# if (goodLines > 50):
			#     break

			avgX = (line[0][0] + line[0][2]) / 2
			avgY = (line[0][1] + line[0][3]) / 2

			# if (avgX <=150):
			#     print 'DETECT IF THE COLOR IS ~WHITE' + frame[avgX][avgY]

			cv2.circle(frame, (avgX, avgY), 5, get_color_by_angle(angle), -1)

			linesWithLabel[get_group_id_by_angle(angle)].append([avgX, avgY])
			linesWithLabelColor[get_group_id_by_angle(angle)].append(get_color_by_angle(angle))

			pt1 = (line[0][0], line[0][1])
			pt2 = (line[0][2], line[0][3])
			cv2.line(frame, pt1, pt2, get_color_by_angle(angle), 2)
			cv2.putText(frame, str(angle), (line[0][0], line[0][1]), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

	# print str(left) + '--' + str(right)
	if (right > 3):
		print 'right' + str(right)
		cv2.putText(frame, 'right swing', (500, 100), font, 2, (0, 0, 0), 1, cv2.LINE_AA)
		os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/beep.mp3 &')
	if (left > 3):
		print 'left' + str(left)
		cv2.putText(frame, 'left swing', (100, 100), font, 2, (0, 0, 0), 1, cv2.LINE_AA)
		os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/beep.mp3 &')


	show_frame(edged, frame, video)














