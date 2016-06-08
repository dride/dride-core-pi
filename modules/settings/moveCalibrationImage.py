import web
import sys
from os import path
sys.path.append( path.dirname (path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
from config import *


urls = (
    '/', 'index'
)

class index:



	@classmethod
	def GET(self):

		data = web.input()
		# reload config
		config = Config()
		innerConfig = config.getConfig()
		if data.direction != 'NaN':
			try:
				if data.direction == 'up':
					config.updateConfigNode('calibration', 'y1', str(innerConfig['y1'] - 10))
				if data.direction == 'down':
					config.updateConfigNode('calibration', 'y1', str(innerConfig['y1'] + 10))
				if data.direction == 'left':
					config.updateConfigNode('calibration', 'x1', str(innerConfig['x1'] - 10))
				if data.direction == 'right':
					config.updateConfigNode('calibration', 'x1', str(innerConfig['x1'] + 10))
			except IOError:

				e = sys.exc_info()[0]
				print  "<p>Error: %s</p>" % e

		return '{"status": "'+str(data.action)+'"}'


if __name__ == "__main__" and __package__ is None:

	app = web.application(urls, globals())
	app.run()