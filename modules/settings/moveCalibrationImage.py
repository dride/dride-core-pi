import web
from config import *

urls = (
    '/', 'index'
)

class index:

	# reload config
	config = Config().getConfig()

	@classmethod
	def GET(self):
		data = web.input()
		if data.action != 'NaN':
			self.config.updateConfigNode('mode', 'in_calibration', data.action)
			self.config.update()

		return '{"status": '+str(data.action)+'}'

if __name__ == "__main__":

	app = web.application(urls, globals())
	app.run()