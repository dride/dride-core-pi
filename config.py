#
#   config file
#   More info : https://github.com/yapQ/cardiganCamVision/wiki/Calibration
#
import ConfigParser, os

# Static globals

# project dir
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
FPS = 4
class Config:


	res = None

	def __init__(self):

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(PARENT_DIR + '/defaults.cfg'))

		if self.config.has_option('calibration', 'FPS') == False:
			# Create initial config file
			self.setInitialConfig()

		self.res = self.prepConfigObj()


	def getConfig(self):

		return self.res

	def setInitialConfig(self):


			self.config.add_section('mode')
			# debug mode
			self.config.set('mode', 'debug', 'True')
			self.config.set('mode', 'in_calibration', 'False')
			self.config.set('mode', 'dvr', 'False')

			self.config.add_section('video')
			# debug mode
			self.config.set('video', 'flip', 'True')

			# gps
			self.config.add_section('gps')
			self.config.set('gps', 'gps', 'True')

			self.config.add_section('calibration')

			# calibration needed
			self.config.set('calibration', 'need_to_calibrate', 'True')

			# FPS
			self.config.set('calibration', 'fps', FPS)

			# X value of avg center of lane
			self.config.set('calibration', 'lane_center', '170')

			# Left upper point of road window
			self.config.set('calibration', 'x1', '50')
			self.config.set('calibration', 'y1', '350')
			self.config.set('calibration', 'road_height', '100')
			self.config.set('calibration', 'road_width', '400')

			# area of interest in fcw width
			self.config.set('calibration', 'square_width', '80')
			self.config.set('calibration', 'square_height', '50')

			# activation speed
			self.config.set('calibration', 'activation_speed', '40')

			# Writing our configuration file to 'example.cfg'
			with open(PARENT_DIR + '/defaults.cfg', 'wb') as configfile:
				self.config.write(configfile)

	def updateConfigNode(self, where, what, val):
		self.config.set(where, what, val)
		# Writing our configuration file to 'example.cfg'
		with open(PARENT_DIR + '/defaults.cfg', 'wb') as configfile:
			self.config.write(configfile)

		self.res = self.prepConfigObj()

	def prepConfigObj(self):
		res = {}
		for each_section in self.config.sections():
			for (key, val) in self.config.items(each_section):
				try:
					res[key] = int(val)
				except ValueError:
					res[key] = self.str2bool(val)

		return res

	@classmethod
	def str2bool(self, v):
		return v.lower() in ("true")