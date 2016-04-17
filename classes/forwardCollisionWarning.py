import cv2
import numpy as np
from classes.sound import sound
import math

class forwardCollisionWarning:

	sound = None
	font = cv2.FONT_HERSHEY_SIMPLEX

	def __init__(self, frame, x1, y1, x2, y2):
		self.frame = frame
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.sound = sound()

		self.watch_for_forward_collision_corners()

	def watch_for_forward_collision(self):

		self.frame = cv2.flip(self.frame, -1)
		self.frame = cv2.flip(self.frame, 1)
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

	def watch_for_forward_collision_corners(self):

		self.frame = cv2.flip(self.frame, -1)
		self.frame = cv2.flip(self.frame, 1)

		cv2.rectangle(self.frame, (self.x1, self.y1), (self.x2, self.y2), (255, 0, 0), 2)

		frame2 = self.frame

		self.frame = self.frame[self.y1:self.y2, self.x1:self.x2]

		sigma = 0.33
		v = np.median(self.frame)
		gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

		# apply automatic Canny edge detection using the computed median
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(gray, lower, upper)

		corners = cv2.goodFeaturesToTrack(edged, 500, 0.4, 10)
		if corners is not None:
			corners = np.int0(corners)

			cornerCount = 0
			for i in corners:
				x, y = i.ravel()

				# make sure the corner is not on the border
				if 0 <= x <= 1 or 0 <= y <= 1 or self.x1-1 <= x <= self.x1+1 or self.y1+1 <= y <= self.y1+1:
					continue
				else:
					cornerCount += 1
					# cv2.circle(self.frame, (x, y), 3, 255, -1)

			cv2.imshow('video23', frame2)
			print cornerCount
			if cornerCount > 8:
				print "found"
				cv2.rectangle(self.frame, (self.x1, self.y1), (self.x2, self.y2), (0, 250, 0), 2)
				cv2.putText(self.frame, "WARNING", (0, 0), self.font, 0.6, (51, 51, 51), 1,
				            cv2.LINE_AA)
				self.sound.play_sound('carAhead', False)


				return 1



		return 0
