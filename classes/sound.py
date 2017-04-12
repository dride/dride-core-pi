import os
import time
from config import *

class sound(object):

	isPlaying = False
	lastPlayed = int(round(time.time() * 1000))
	raspberry = False

	def __init__(self):
		self.isPlaying = False



	def play_sound(self, type, urgent):

		self.updateIsPlaying()

		if self.isPlaying == False:
			self.isPlaying = True
			if self.raspberry == False:
				os.system('mpg321 ' + PARENT_DIR + '/assets/sound/'+str(type)+'.mp3 &')
			else:
				os.system('mpg123 ' + PARENT_DIR + '/assets/sound/' + str(type) + '.mp3 &')
			self.isPlaying = False

	def updateIsPlaying(self):
		lp =  int(round(time.time() * 1000))

		if int(lp) - int(self.lastPlayed) > 1000:
			self.isPlaying = False
			self.lastPlayed = lp
		else:
			self.isPlaying = True