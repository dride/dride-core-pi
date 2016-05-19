import os
from config import *

class GPS:


	def __init__(self):

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(PARENT_DIR + '/defaults.cfg'))

		if self.config.has_option('calibration', 'FPS') == False:
			# Create initial config file
			self.setInitialConfig()

		self.res = self.prepConfigObj()

	def change_active_file(self, fileName):

		return self.res

