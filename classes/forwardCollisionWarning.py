import cv2
import numpy as np
from classes.sound import sound
import math

class forwardCollisionWarning:

	sound = sound()
	font = cv2.FONT_HERSHEY_SIMPLEX

	def __init__(self, frame, x1, y1, x2, y2):
		self.frame = frame
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

		self.watch_for_forward_collision_perpendicular_lines()

	def watch_for_forward_collision(self):

		# self.frame = cv2.flip(self.frame, -1)
		# self.frame = cv2.flip(self.frame, 1)

		self.frame = self.frame[self.y1:self.y2, self.x1:self.x2]

		cascade_src = '/Users/saoron/cardiganCam/assets/haar/cars.xml'
		car_cascade = cv2.CascadeClassifier(cascade_src)

		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		cars = car_cascade.detectMultiScale(self.frame, 1.1, 1)

		for (x, y, w, h) in cars:
			avgX = int(x + w / 2)
			avgY = int(y + h / 2)

			dy = avgX - 0
			dx = avgY - 0
			angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

			cv2.rectangle(self.frame, (x, y), (x + w, y + h), (51, 51, 51), 2)

		cv2.imshow('video4', self.frame)

	def watch_for_forward_collision_perpendicular_lines(self):

		# self.frame = cv2.flip(self.frame, -1)
		# self.frame = cv2.flip(self.frame, 1)

		cv2.rectangle(self.frame, (self.x1, self.y1), (self.x2, self.y2), (255, 0, 0), 1)

		frame2 = self.frame

		self.frame = self.frame[self.y1:self.y2, self.x1:self.x2]

		sigma = 0.33
		v = np.median(self.frame)
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

		# apply automatic Canny edge detection using the computed median
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(gray, lower, upper)


		lines = cv2.HoughLinesP(edged, 1, math.pi / 360,  6, 10, 10);
		if (lines is not None):
			for line in lines:

				dy = line[0][3] - line[0][1];
				dx = line[0][2] - line[0][0];
				angle = int(math.atan2(dy, dx) * 180.0 / math.pi);

				if (angle != 0):
					continue

				pt1 = (line[0][0], line[0][1])
				pt2 = (line[0][2], line[0][3])
				if  line[0][1] == 0 or line[0][1] == 1:
					continue

				cv2.line(self.frame, pt1, pt2, (255, 0, 255), 2)
				cv2.putText(self.frame,  str(line[0][1]), (int(line[0][0] / 2), line[0][1]), self.font, 0.5, (51, 51, 51), 1, cv2.LINE_AA)



				# print 'corner ' + str(cornerCount)
				if lines is not None:
					print 'lines ' + str(len(lines))
				if line[0][1] > 25:
					print "found"

					cv2.rectangle(self.frame, (self.x1, self.y1), (self.x2, self.y2), (0, 250, 0), 2)
					cv2.putText(self.frame, "WARNING", (100, 100), self.font, 1, (255, 255, 255), 1,
					            cv2.LINE_AA)
					self.sound.play_sound('carAhead', False)


					return 1
			cv2.imshow('video23', frame2)


		return 0
