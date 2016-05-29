from config import *
from classes.laneDepartureWarning import laneDepartureWarning

class calibration:

	frame = None
	cleanFrame = None
	# load config
	configObj = Config()
	config = configObj.getConfig()


	def __init__(self):

		self.frame = None

	def needToCalibrate(self):

		return self.config['need_to_calibrate']

	def calibrate(self, frame):

		##########################################################################
		# TODO: think of a way to do this on a set of frames and use avg to find
		# the best calibration
		##########################################################################


		self.frame = frame.copy()
		self.cleanFrame = frame.copy()
		avgX  = avgY = 0
		avgX_C = avgY_C = 0

		for y1 in xrange(100, 250, 10):
			for x1 in xrange(0, 200, 10):
				roadFrame = self.frame[y1:y1 + self.config['road_height'], x1:x1 + self.config['road_width']]

				ldw = laneDepartureWarning(roadFrame, self.config['lane_center'], True, self.cleanFrame)
				ldw.lifePeriod = 0
				# laneCenter = ldw.find_lanes(False)

				if ldw.finalCenterPointsCount >= 3 and ldw.notTooFarAwaPoints(ldw.finalCenterPoints, 10):
					avgX += x1
					avgX_C += 1
					avgY += y1
					avgY_C += 1


				self.frame = frame.copy()
				self.cleanFrame = frame.copy()

		ldw.lifePeriod = 60
		if avgX_C > 0 and avgY_C > 0:
			self.configObj.updateConfigNode('calibration', 'need_to_calibrate', 'False')
			self.configObj.updateConfigNode('calibration', 'x1', str(int(avgX / avgX_C)))
			self.configObj.updateConfigNode('calibration', 'y1', str(int(avgY / avgY_C)))


