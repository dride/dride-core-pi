import cv2
import numpy as np
import os
import math

class laneDepartureWarning:

	font = cv2.FONT_HERSHEY_SIMPLEX
	width = 500
	height = 300

	numberOfChuncks = 9

	def __init__(self, frame, flip, video):
		self.frame = frame
		self.find_lanes(flip, video)


	# Find lanes using angle
	def find_lanes(self, flip, video):
		linesWithLabel = [[], [], [], [], [], [], [], [], [], [], [], []]
		linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], [], []]
		self.linesInGroups_left = [[], [], [], [], [], [], [], [], [], []]
		self.linesInGroups_right = [[], [], [], [], [], [], [], [], [], []]

		if flip:
			self.frame = self.frame[100:275, 0:500]
			self.frame = cv2.flip(self.frame, -1)
			self.frame = cv2.flip(self.frame, 1)


		sigma = 0.33
		v = np.median(self.frame)
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)


		# apply automatic Canny edge detection using the computed median
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(gray, lower, upper)

		# super sensitive
		# lines = cv2.HoughLinesP(edged, 1, math.pi / 360, 6, 30, 6);

		lines = cv2.HoughLinesP(edged, 1, math.pi / 360, 9, 30, 9);
		filteredLines = []
		linesWithLabel = [[], [], [], [], [], [], [], [], [], [], [], []]
		groupedLines = [[], [], [], [], [], [], [], [], [], [], [], []]
		linesWithLabelColor = [[], [], [], [], [], [], [], [], [], [], [], []]
		right = 0
		left = 0

		# split road to chuncks
		for chunk in range(0, self.numberOfChuncks):
			fromPt = 0, chunk*25
			toPt = 500, chunk*25
			# cv2.line(self.frame, fromPt, toPt, (255, 255, 255, 0.5), 1)



		if (lines is not None) :
			for line in lines:

				dy = line[0][3] - line[0][1];
				dx = line[0][2] - line[0][0];
				angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

				if (angle == 90 or angle == -90 or angle == 0 or angle > -20 and angle < 20):
					continue

				# insert to filtered lines array
				filteredLines.append(line)

				if (angle > 60 and angle <= 90):
					right += 1
				if (angle < -60 and angle >= -90):
					left += 1

				# if (((angle < -30 and angle >= -45) or (angle > 30 and angle <= 45)) == False):
				# 	continue
				#

				pt1 = (line[0][0], line[0][1])
				pt2 = (line[0][2], line[0][3])
				# # experimenal - if too many line > 50 we can stop looking
				# # Migt be problamatic in case of departure
				# goodLines += 1
				# if (goodLines > 50):
				#     break

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


		# detect lane side
		self.predict_lane(filteredLines)

		# detect center of each sector
		self.get_avg_of_secotors()


		# self.draw_lines_by_arr(self.linesInGroups_right)
		# self.draw_lines_by_arr(self.linesInGroups_left)


		# print str(left) + '--' + str(right)
		if (right > 3):
			print 'right ' + str(right)
			cv2.putText(self.frame, 'right swing', (500, 100), self.font, 2, (0, 0, 0), 1, cv2.LINE_AA)
			os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/beep.mp3 &')
		if (left > 3):
			print 'left ' + str(left)
			cv2.putText(self.frame, 'left swing', (100, 100), self.font, 2, (0, 0, 0), 1, cv2.LINE_AA)
			os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/beep.mp3 &')


		self.show_frame(edged, self.frame, video)

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

	def show_frame(self, frame1, frame2, video):

		cv2.imshow('img1', frame1)
		cv2.imshow('img2', frame2)

		if video:
			cv2.waitKey(27)
		else:
			cv2.waitKey(0)

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
			cv2.rectangle(self.frame, (0, 0), (100 , 30), (255, 255, 255), -1);

			if left > right:
				lane = "Left Lane"
			else:
				lane = "Right Lane"

			cv2.putText(self.frame, lane, (10, 20), self.font, 0.5, (51, 51, 51), 1, cv2.LINE_AA)

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
		finalCenterPoints  = []
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

			if len(right_lane_candidtae) > 0 and len(left_lane_candidtae) > 0:

				ptR1 = (right_lane_candidtae[0][0], right_lane_candidtae[0][1])
				ptR2 = (right_lane_candidtae[0][2], right_lane_candidtae[0][3])
				ptL1 = (left_lane_candidtae[0][0], left_lane_candidtae[0][1])
				ptL2 = (left_lane_candidtae[0][2], left_lane_candidtae[0][3])

				avgX_R = (right_lane_candidtae[0][0] + right_lane_candidtae[0][2]) / 2
				avgY_R = (right_lane_candidtae[0][1] + right_lane_candidtae[0][3]) / 2

				avgX_L = (left_lane_candidtae[0][0] + left_lane_candidtae[0][2]) / 2
				avgY_L = (left_lane_candidtae[0][1] + left_lane_candidtae[0][3]) / 2

				dy = avgY_L - avgY_R;
				dx = avgX_L - avgX_R;
				angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

				centerChunkX = (avgX_R + avgX_L) / 2
				centerChunkY = (avgY_R + avgY_L) / 2

				finalCenterPoints.append((centerChunkX, centerChunkY))

				cv2.circle(self.frame, (avgX_R, avgY_R), 5, self.get_color_by_angle(-40), -1)
				cv2.circle(self.frame, (avgX_L, avgY_L), 5, self.get_color_by_angle(-40), -1)
				cv2.line(self.frame, (avgX_R, avgY_R), (avgX_L, avgY_L), self.get_color_by_angle(-26), 1)

				cv2.circle(self.frame, (centerChunkX, centerChunkY), 5, self.get_color_by_angle(-15), -1)
				cv2.putText(self.frame, str(angle), (centerChunkX+10, centerChunkY), self.font, 0.6, (51, 51, 51), 1, cv2.LINE_AA)


				cv2.line(self.frame, ptR1, ptR2, self.get_color_by_angle(0), 2)
				cv2.line(self.frame, ptL1, ptL2, self.get_color_by_angle(10), 2)

		# draw center of lane
		count = 0
		sum = 0

		for pt in finalCenterPoints:
			sum += pt[0]
			count+=1
		# mark center
		if count > 0:
			cv2.line(self.frame, (sum/count, 0), (sum/count, self.height), (0, 0, 255), 2)


	def assign_group_to_line(self, line):

		for chunk in range(0, self.numberOfChuncks):
			fromY = chunk*25
			toY   = (chunk+1)*25

			if self.intersect( (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, fromY), (self.width, toY)) or (line[0][1] >= fromY and line[0][3] <= toY):
				if self.get_lane_direction_by_point(line):
					self.linesInGroups_left[chunk].append(line)
				else:
					self.linesInGroups_right[chunk].append(line)


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