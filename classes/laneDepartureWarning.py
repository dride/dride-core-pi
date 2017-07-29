import cv2
import numpy as np
import math
from classes.linearEquation import linearEquation
from classes.sound import sound
import time
from config import *
from modules.indicators.python.states.indicators import Indicators


class laneDepartureWarning(object):

	font = cv2.FONT_HERSHEY_SIMPLEX
	height, width = 150,300

	defaultCenter = 250
	laneDir = 0 # -1 left # 1 right
	numberOfChuncks = 30
	lineJump = 5
	lifePeriod = 60 # determine by speed
	flag = 0
	frameClean = None
	frameNumber = 0
	raspberry = False
	# debug picture interval in ms
	captureInterval = 10
	sound = sound()

	# load config
	config = Config().getConfig()

	finalCenterPoints = [[] for i in range(32)]
	finalCenterPointsCount = 0

	def __init__(self, frame, laneCenter, raspberry, frameClean, frameNumber):
		self.frame = frame
		self.frameClean = frameClean
		self.defaultCenter = laneCenter
		self.raspberry = raspberry
		self.sound.raspberry = raspberry
		self.frameNumber = frameNumber

	# Find lanes using angle
	def find_lanes(self, video):
		linesWithLabel = [[] for i in range(12)]
		linesWithLabelColor = [[] for i in range(12)]
		self.linesInGroups_left = [[] for i in range(64)]
		self.linesInGroups_right = [[] for i in range(64)]

		# update config
		self.config = Config().getConfig()

		# # save frames in debug mode
		# if self.config['debug']:
		# 	millis = int(round(time.time() * 1000))
		# 	if millis % self.captureInterval == 0:
		# 		cv2.imwrite(PARENT_DIR + "/training/timed/" + str(millis) + ".jpg", self.frame)

		sigma = 0.33
		v = np.median(self.frame)
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)



		# apply automatic Canny edge detection using the computed median
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(gray, lower, upper)


		# good for highway streight
		# lines = cv2.HoughLinesP(edged, 1, math.pi / 180, 50, 10, 10);
		# TODO: This settings affect lane departure!
		lines = cv2.HoughLinesP(edged, 1, math.pi / 360,  6, 30, 6);

		filteredLines = []
		linesWithLabel = [[] for i in range(12)]
		groupedLines = [[] for i in range(12)]
		linesWithLabelColor = [[] for i in range(12)]
		right = 0
		left = 0

		# split road to chuncks
		for chunk in range(0, self.numberOfChuncks):
			fromPt = 0, chunk*self.lineJump
			toPt = 500, chunk*self.lineJump
			# cv2.line(self.frame, fromPt, toPt, (255, 255, 255, 0.5), 1)



		if (lines is not None) :
			for line in lines:



				dy = line[0][3] - line[0][1];
				dx = line[0][2] - line[0][0];
				angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

				if (angle == 90 or angle == -90 or angle == 0):
					continue

				# insert to filtered lines array
				filteredLines.append(line)

				if (angle > 60 and angle <= 90):
					right += 1
					print right
					print
				if (angle < -60 and angle >= -90):
					left += 1

				# if ( (-45 <= angle < -30 or 30 < angle <= 45) == False):
				# 	continue

				pt1 = (line[0][0], line[0][1])
				pt2 = (line[0][2], line[0][3])

				avgX = (line[0][0] + line[0][2]) / 2
				avgY = (line[0][1] + line[0][3]) / 2

				# if (avgX <=150):
				#     print 'DETECT IF THE COLOR IS ~WHITE' + self.frame[avgX][avgY]

				# cv2.circle(self.frame, (pt1), 5, self.get_color_by_angle(angle), -1)
				# cv2.circle(self.frame, (pt2), 5, self.get_color_by_angle(angle), -1)

				groupedLines[self.get_group_id_by_angle(angle)].append([(line[0][0], line[0][1]), (line[0][2], line[0][3])])
				linesWithLabel[self.get_group_id_by_angle(angle)].append([avgX, avgY])
				linesWithLabelColor[self.get_group_id_by_angle(angle)].append(self.get_color_by_angle(angle))


				# cv2.line(self.frame, pt1, pt2, self.get_color_by_angle(angle), 2)
				# cv2.putText(self.frame, str(angle), (line[0][0]+20, line[0][1]), self.font, 0.6, (51, 51, 51), 1, cv2.LINE_AA)

				# append line to its horizontal group
				self.assign_group_to_line(line)

		# draw virtual lanes
		# self.add_virtual_lines()

		# detect lane side
		self.predict_lane(filteredLines)

		# detect center of each sector
		self.get_avg_of_secotors()


		# self.draw_lines_by_arr(self.linesInGroups_right)
		# self.draw_lines_by_arr(self.linesInGroups_left)

		if (right > 3):
			print 'right ' + str(right)

			cv2.putText(self.frame, 'right swing', (100, 100), self.font, 2, (0, 0, 0), 1, cv2.LINE_AA)
			if self.config['debug'] == True:
				millis = int(round(time.time() * 1000))
				cv2.imwrite(PARENT_DIR + "/training/road/" + str(millis) + "_right.jpg", self.frameClean)

			self.sound.play_sound('laneDeparture', False)
			# turn indicator
			indicator = Indicators()
			indicator.rightLaneDeparture()


			self.clear_center_point()
		if (left > 3):
			print 'left ' + str(left)

			cv2.putText(self.frame, 'left swing', (100, 100), self.font, 2, (0, 0, 0), 1, cv2.LINE_AA)
			if self.config['debug'] == True:
				millis = int(round(time.time() * 1000))
				cv2.imwrite(PARENT_DIR + "/training/road/" + str(millis) + "_left.jpg", self.frameClean)

			self.sound.play_sound('laneDeparture', False)
			# turn indicator
			indicator = Indicators()
			indicator.leftLaneDeparture()

			self.clear_center_point()


		if self.raspberry == False:
			self.show_frame(edged, self.frame, video)

		if self.config['in_calibration'] == True and self.frameNumber % 4 == 0:
			# save road
			cv2.imwrite(PARENT_DIR + "/modules/settings/road.jpg", self.frame)

		# # save frames in debug mode
		# if self.config['debug'] and self.finalCenterPointsCount >= 2 and self.notTooFarAwaPoints(self.finalCenterPoints, 10):
		# 	millis = int(round(time.time() * 1000))
		# 	cv2.imwrite(PARENT_DIR + "/training/timed/" + str(millis) + ".jpg", self.frame)

		return self.get_avg_center_X()


	# return if the point are close to each other by -distance (Pixles)
	@classmethod
	def notTooFarAwaPoints(self, finalCenterPoints, distance):
		maxX = maxY = 0
		minX = minY = 1000
		for i in range(len(finalCenterPoints)):

			if finalCenterPoints[i] and finalCenterPoints[i][0][0] < minX:
				minX = finalCenterPoints[i][0][0]

			if finalCenterPoints[i] and finalCenterPoints[i][0][0] > maxX:
				maxX = finalCenterPoints[i][0][0]

			if finalCenterPoints[i] and finalCenterPoints[i][0][1] < minY:
				minY = finalCenterPoints[i][0][1]

			if finalCenterPoints[i] and finalCenterPoints[i][0][1] > maxY:
				maxY = finalCenterPoints[i][0][1]

		return abs(minY - maxY) < distance and abs(minX - maxX) < distance

	@classmethod
	def show_frame(self, frame1, frame2, video):

		cv2.imshow('img1', frame1)
		cv2.imshow('img2', frame2)

		if video:
			cv2.waitKey(27)
		else:
			cv2.waitKey(0)

	@classmethod
	def color_variant(self, hex_color, brightness_offset=1):
		""" takes a color like #87c95f and produces a lighter or darker variant """
		if len(hex_color) != 7:
			raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
		rgb_hex = [hex_color[x:x + 2] for x in [1, 3, 5]]
		new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
		new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]  # make sure new values are between 0 and 255
		return new_rgb_int

	# predict what lane are we in
	def predict_lane(self, lines, debug = True):
		right = 0
		left = 0
		lane = ''
		for line in lines:

			if self.get_lane_direction_by_point(line):
				left += 1
			else:
				right +=1
		if debug:
			if left > right:
				laneDir = -1
			else:
				laneDir = 1

			cv2.putText(self.frameClean, lane, (10, 20), self.font, 0.5, (51, 51, 51), 1, cv2.LINE_AA)

		return left > right

	# Return True if point is in Left lane
	def get_lane_direction_by_point(self, line):
		right = 0
		left = 0

		avgX = (line[0][0] + line[0][2]) / 2

		if avgX > self.width / 2:
			right += 1
		else:
			left += 1

		return left > right

	def get_avg_of_secotors(self):

		for chunk in range(0, self.numberOfChuncks):
			#setup minimum value for right lane
			min = self.width
			right_lane_candidtae = ''
			#setup maximum value for left lane
			max = 0
			left_lane_candidtae = ''
			# left lane inspection
			if (self.linesInGroups_left[chunk] is not None) :
				for line in self.linesInGroups_left[chunk]:
					# compare the X value to find the closest point to the center
					# looking for maximum
					if line[0][0] > max:
						max = line[0][0]
						left_lane_candidtae = line
			# right lane inspection
			if (self.linesInGroups_right[chunk] is not None):
				for line in self.linesInGroups_right[chunk]:
					# compare the X value to find the closest point to the center
					# looking for maximum
					if line[0][0] < min:
						min = line[0][0]
						right_lane_candidtae = line

			self.remove_aged_centers(chunk)

			# if we found parallel lines on chunk
			if len(right_lane_candidtae) > 0 and len(left_lane_candidtae) > 0:

				ptR1 = (right_lane_candidtae[0][0], right_lane_candidtae[0][1])
				ptR2 = (right_lane_candidtae[0][2], right_lane_candidtae[0][3])
				ptL1 = (left_lane_candidtae[0][0], left_lane_candidtae[0][1])
				ptL2 = (left_lane_candidtae[0][2], left_lane_candidtae[0][3])


				# cv2.line(self.frame, (ptR1), (ptR2), self.get_color_by_angle(-26), 2)
				# cv2.line(self.frame, (ptL1), (ptL2), self.get_color_by_angle(26), 2)
				#
				# cv2.circle(self.frame, (ptR1), 2, self.get_color_by_angle(-15), -1)
				# cv2.circle(self.frame, (ptR2), 2, self.get_color_by_angle(-35), -1)
				#
				# cv2.circle(self.frame, (ptL1), 2, self.get_color_by_angle(15), -1)
				# cv2.circle(self.frame, (ptL2), 2, self.get_color_by_angle(35), -1)

				equation = linearEquation(ptR1, ptR2)
				estimatedPointR = equation.getX(chunk * self.lineJump), chunk * self.lineJump
				# cv2.circle(self.frame, (estimatedPointR), 5, self.get_color_by_angle(15), -1)

				equation = linearEquation(ptL1, ptL2)
				estimatedPointL = equation.getX(chunk * self.lineJump), chunk * self.lineJump
				# cv2.circle(self.frame, (estimatedPointL), 5, self.get_color_by_angle(45), -1)

				avgX_R = estimatedPointR[0]
				avgY_R = estimatedPointR[1]

				avgX_L = estimatedPointL[0]
				avgY_L = estimatedPointL[1]

				dy = avgY_L - avgY_R;
				dx = avgX_L - avgX_R;
				angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

				centerChunkX = (avgX_R + avgX_L) / 2
				centerChunkY = (avgY_R + avgY_L) / 2

				############################
				# This part check if the length of the line to big
				# should be a linear formula
				# curnetly we remove too long lines on top of the road
				# TODO: imporve this part
				############################
				crossLine = linearEquation(estimatedPointR, estimatedPointL)
				if (0 <= chunk <= 5 and crossLine.calculateDistance() > 180) or (5 < chunk <= 8 and crossLine.calculateDistance() > 250):
					continue

				############################
				# This part works great on straight lines
				# it should be dynamic in case of turns
				# curnetly we set a trash hold of 90 % from the middle avg
				# TODO: inspect the range in curves
				############################

				# get color samples near our object to detect doubled lines
				roadColorRight =  self.frame[self.get_probe_safe(avgY_R , avgX_R-20)]
				rightColor =  self.frame[self.get_probe_safe(avgY_R, avgX_R-3)]


				roadColorLeft =  self.frame[self.get_probe_safe(avgY_L, avgX_L+40)]
				leftColor =  self.frame[self.get_probe_safe(avgY_L, avgX_L+3)]


				if  95 < (100 * centerChunkX) / self.get_lane_avg_x() < 105 and self.if_color_in_range(roadColorRight, rightColor, 70) and self.if_color_in_range(roadColorLeft, leftColor, 70):
					self.finalCenterPoints[chunk] = [(centerChunkX, centerChunkY), self.lifePeriod]  # point , age
					self.finalCenterPointsCount += 1

					# # add more point down and up stream
					# equation = linearEquation(ptL1, ptL2)
					# for i in range(0, self.numberOfChuncks):
					# 	estimatedPointL =  equation.getX((i) * self.lineJump), (i) * self.lineJump
					# 	cv2.circle(self.frame, (estimatedPointL), 5, self.get_color_by_angle(45), -1)
					#
					# equation = linearEquation(ptR1, ptR2)
					# for i in range(0, self.numberOfChuncks):
					# 	estimatedPointR = equation.getX((i) * self.lineJump), (i) * self.lineJump
					# 	cv2.circle(self.frame, (estimatedPointR), 5, self.get_color_by_angle(45), -1)

					cv2.circle(self.frame, (avgX_R, avgY_R), 5, (255, 255, 255), -1)
					cv2.circle(self.frame, (avgX_L, avgY_L), 5, (255, 255, 255), -1)

					cv2.line(self.frame, (avgX_R, avgY_R), (avgX_L, avgY_L), self.get_color_by_angle(-26), 1)

					cv2.circle(self.frame, (centerChunkX, centerChunkY), 5, self.get_color_by_angle(-15), -1)
					cv2.putText(self.frame, str((100 * centerChunkX) / self.get_lane_avg_x()), (centerChunkX+10, centerChunkY), self.font, 0.6, (51, 51, 51), 1, cv2.LINE_AA)


					cv2.line(self.frame, ptR1, ptR2, self.get_color_by_angle(0), 2)
					cv2.line(self.frame, ptL1, ptL2, self.get_color_by_angle(10), 2)

		# self.clear_line_if_all_points_are_old()

		# self.draw_center_polyfit_line()

		self.draw_center_circles()

		self.draw_center_avg_line()

	def assign_group_to_line(self, line):

		for chunk in range(0, self.numberOfChuncks):
			fromY = chunk*self.lineJump
			toY   = (chunk+1)*self.lineJump

			# if we intersect with one of the horizontal delimiters or we are on a delimiter
			if self.intersect( (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, fromY), (self.width, toY)) or (line[0][1] >= fromY and line[0][3] <= toY):

				if self.get_lane_direction_by_point(line):
					self.linesInGroups_left[chunk].append(line)
				else:
					self.linesInGroups_right[chunk].append(line)

	@classmethod
	def ccw(self, A, B, C):
		return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

	# Return true if line segments AB and CD intersect
	def intersect(self, A, B, C, D):
		return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

	def draw_lines_by_arr(self, lines):

		for chunk in range(0, self.numberOfChuncks):
			if (lines[chunk] is not None) :
				for line in lines[chunk]:
					if len(line) > 0:
						pt1 = (line[0][0], line[0][1])
						pt2 = (line[0][2], line[0][3])
						cv2.line(self.frame, pt1, pt2, self.get_color_by_angle(chunk*15), 2)

	# Return X avg of in-memory center
	def get_lane_avg_x(self):
		sum = 0
		count = 0
		for pt in self.finalCenterPoints:
			if len(pt) > 0:
				sum += pt[0][0]
				count += 1
		return sum / count if count > 0 else self.defaultCenter

	def remove_aged_centers(self, chunk):
		if len(self.finalCenterPoints[chunk]) > 0:
			self.finalCenterPoints[chunk][1] -= 1

		if len(self.finalCenterPoints[chunk]) > 0 and self.finalCenterPoints[chunk][1] <= 0:
			self.finalCenterPoints[chunk] = []

	def get_avg_center_X(self):
		# draw center of lane
		count = 0
		sum = 0

		for pt in self.finalCenterPoints:
			if len(pt) > 0:
				sum += pt[0][0]
				count += 1
		# mark center
		return sum / count if count > 0 else self.defaultCenter


	def draw_center_avg_line(self):
		# draw center of lane
		avg = self.get_avg_center_X()
		cv2.line(self.frame, (avg, self.height / 2), (avg, self.height), (0, 255, 255), 2)


	def draw_center_polyfit_line(self):
		# fit line algo
		pts = []
		# generate two arrays for X and Y for polyfit
		for pt in self.finalCenterPoints:
			if len(pt) > 0:
				pts.append((pt[0][0], pt[0][1]))

		if len(pts) > 0:
			rows = self.height
			cols = self.width
			[vx, vy, x, y] = cv2.fitLine(np.array(pts), cv2.DIST_L2, 0, 0.01, 0.01)
			lefty = int((-x * vy / vx) + y)
			righty = int(((cols - x) * vy / vx) + y)
			if self.inInt(lefty) and self.inInt(righty):
				cv2.line(self.frame, (cols, righty), (0, lefty), (0, 0, 255), 2)


	def draw_center_circles(self):
		# print cicrles in ceter with memory
		for pt in self.finalCenterPoints:
			if len(pt) > 0:
				cv2.circle(self.frame, (pt[0][0], pt[0][1]), 2, self.get_color_by_angle(55), -1)

	def add_virtual_lines(self):
		print '---'
		print len(self.linesInGroups_right[2])

		# equation = linearEquation(ptR1, ptR2)
		# estimatedPointR = equation.getX(chunk * self.lineJump), chunk * self.lineJump

	# clear all centered points
	def clear_center_point(self):
		for chunk in range(0, self.numberOfChuncks):
			if len(self.finalCenterPoints[chunk]) > 0:
				self.finalCenterPoints[chunk][1] = 0

	# return which lane
	def get_lane(self):
		if self.laneDir == -1:
			return 'Left Lane'
		else:
			return  'Right Lane'



	# clear all centered points
	def clear_line_if_all_points_are_old(self):
		for chunk in range(0, self.numberOfChuncks):
			if len(self.finalCenterPoints[chunk]) > 0 and self.lifePeriod - 5 <= self.finalCenterPoints[chunk][1]:
				return False
		print "clear"
		self.clear_center_point()

	# will return the x,y with respect to borders
	def get_probe_safe(self, avgY, avgX):

		if avgX  >= self.width:
			avgX =  self.width - 1
		if avgX < 0:
			avgX = 0

		if avgY >= self.height:
			avgY = self.height - 1
		if avgY < 0:
			avgY = 0

		return (avgY, avgX)

	@classmethod
	def if_color_in_range(self, baseColor, cmpColor, trashold):


		if not trashold < int(cmpColor[0])*100 / int(baseColor[0]+1) < 200 - trashold:
			return False
		if not trashold < int(cmpColor[1])*100 / int(baseColor[1]+1) < 200 - trashold:
			return False
		if not trashold < int(cmpColor[1])*100 / int(baseColor[2]+1) < 200 - trashold:
			return False

		return True

	@classmethod
	def inInt(self, num):
		return -5000000 < num < 5000000

	@classmethod
	def get_color_by_angle(self, angle):
		if 10 < angle <= 15:
			return 245, 12, 12
		if 15 < angle <= 28:
			return 245, 12, 184
		if 28 < angle <= 40:
			return 134, 12, 245
		if 40 < angle <= 45:
			return 12, 83, 245
		if 45 < angle <= 55:
			return 12, 245, 159

		if -15 < angle >= -10:
			return 47, 245, 12
		if -10 < angle >= -15:
			return 187, 245, 12
		if -15 < angle >= -28:
			return 245, 173, 12
		if -28 < angle >= -40:
			return 245, 4, 12
		if -40 < angle >= -45:
			return 0, 0, 250
		if -45 < angle >= -55:
			return 12, 65, 19

		# default color
		return 0, 255, 255

	@classmethod
	def get_group_id_by_angle(self, angle):
		if 10 < angle <= 15:
			return 1
		if 15 < angle <= 28:
			return 2
		if 25 < angle <= 35:
			return 3
		if 28 < angle <= 40:
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