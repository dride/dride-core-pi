import web

urls = (
    '/', 'index'
)

class index:

	def GET(self):
		data = web.input()
		if data.heading != 'NaN':
			with open('gps.json', 'w') as file_:
				file_.write(data.heading)

		return data.heading

if __name__ == "__main__":

	app = web.application(urls, globals())
	app.run()