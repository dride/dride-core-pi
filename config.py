#
#   config file
#   More info : https://github.com/yapQ/cardiganCamVision/wiki/Calibration
#
import ConfigParser, os

# Static globals

# project dir
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:


	res = None

	def __init__(self):

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(PARENT_DIR + '/defaults.cfg'))

		if self.config.has_option('calibration', 'FPS') == False:
			# Create initial config file
			self.setInitialConfig()

		self.res =  self.prepConfigObj()


	def getConfig(self):

		return  self.res

	def setInitialConfig(self):


			self.config.add_section('mode')
			# debug mode
			self.config.set('mode', 'debug', 'True')

			self.config.add_section('calibration')

			# FPS
			self.config.set('calibration', 'FPS', '8')

			# X value of avg center of lane
			self.config.set('calibration', 'lane_center', '100')

			# Left upper point of road window
			self.config.set('calibration', 'x1', '150')
			self.config.set('calibration', 'y1', '170')
			self.config.set('calibration', 'road_height', '250')
			self.config.set('calibration', 'road_width', '300')

			# delta for where to find cars square
			self.config.set('calibration', 'deltaX', '160')
			self.config.set('calibration', 'deltaY', '-70')

			# area of interest in fcw width
			self.config.set('calibration', 'SQUARE_WIDTH', '160')

			# Writing our configuration file to 'example.cfg'
			with open('defaults.cfg', 'wb') as configfile:
				self.config.write(configfile)

	def updateConfigNode(self, where, what, val):
		self.config.set(where, what, val)
		# Writing our configuration file to 'example.cfg'
		with open('defaults.cfg', 'wb') as configfile:
			self.config.write(configfile)

		self.res = self.prepConfigObj()

	def prepConfigObj(self):
		res = {}
		for each_section in self.config.sections():
			for (key, val) in self.config.items(each_section):
				try:
					res[key] = int(val)
				except:
					res[key] = bool(val)

		return res





