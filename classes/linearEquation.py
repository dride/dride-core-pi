import math


class linearEquation(object):

	def __init__(self, pt1, pt2):
		self.pt1 = pt1
		self.pt2 = pt2

	def get_angle(self):

		return (self.pt2[1] - self.pt1[1]) / float(self.pt2[0] - self.pt1[0])

	# get x coordinate based on linear eqation
	# Y = mx - ma + b | y - b = m( x - a )
	def getX(self, y):

		return int((y + (self.get_angle()*self.pt1[0]) - self.pt1[1]) / float(self.get_angle()))

	def calculateDistance(self):

		return math.hypot(self.pt2[0] - self.pt1[0], self.pt2[1] - self.pt1[1])