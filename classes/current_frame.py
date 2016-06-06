import time
from config import *
from classes.gps import GPS


class CurrentFrame:
	def __init__(self, frame):
		self.frame = frame

	def get_frame(self):
		return self.frame
