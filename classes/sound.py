import os
import pyglet

class sound:

	isPlaying = False

	def __init__(self):
		self.isPlaying = False



	def play_sound(self, type, urgent):

		if self.isPlaying == False:
			self.isPlaying = True
			os.system('mpg321 /Users/saoron/cardiganCam/assets/sound/'+str(type)+'.mp3 &')
			self.isPlaying = False

