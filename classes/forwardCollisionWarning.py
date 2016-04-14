import cv2
import numpy as np
import os

class forwardCollisionWarning:

	def __init__(self, frame, x1, y1, x2, y2):
		self.frame = frame
		self.x1 = 280
		self.y1 = 250
		self.x2 = 320
		self.y2 = 320

		self.watch_for_forward_collision()



	def watch_for_forward_collision(self):

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
					cv2.circle(self.frame, (x, y), 3, 255, -1)

			cv2.imshow('video23', frame2)

			if cornerCount > 9:
				print "found"
				cv2.rectangle(frame2, (self.x1, self.y1), (self.x2, self.y2), (0, 250, 0), 2)
				os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/carBeep.mp3 &')


				return 1



		return 0
