import web
import sys
from os import path
sys.path.append( path.dirname (path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
from config import *


urls = (
    '/', 'index'
)

class index(object):



	@classmethod
	def GET(self):

		data = web.input()
		# reload config
		config = Config()

		if data.action != 'NaN':
			try:
				config.updateConfigNode('mode', 'in_calibration', data.action)
			except IOError:

				e = sys.exc_info()[0]
				print  "<p>Error: %s</p>" % e

		return '{"status": "'+str(data.action)+'"}'


if __name__ == "__main__" and __package__ is None:

	app = web.application(urls, globals())
	app.run()