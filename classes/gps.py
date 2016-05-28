import os
from config import *
import json
import time

class GPS:

	@classmethod
	def getPos(self):

		file = open(PARENT_DIR + "/modules/gps/gps.json", 'r')

		return file.read()

	@classmethod
	def createNewGPSrecordFile(self, filename):

		file = open(PARENT_DIR + "/modules/video/gps/" + filename + ".json", 'w')
		file.write('{}')

	def AppendGPSPositionToCurrentFile(self, fileName):

		timestamp = int(round(time.time()))

		# laod current position object from gps module
		# TODO: use internal GPS module
		currentPosJson = self.getPos()
		a_dict = {timestamp: currentPosJson}

		# # load recorded data for this filename
		# recordedDataJson = open(PARENT_DIR + "/modules/video/gps/"+fileName+".json", 'r')
		# recordedData = json.loads(currentPosJson)
		#
		# recordedData.extend(currentPos)

		with open(PARENT_DIR + "/modules/video/gps/"+fileName+".json") as f:
			data = json.load(f)

		data.update(a_dict)

		with open(PARENT_DIR + "/modules/video/gps/"+fileName+".json", 'w') as f:
			json.dump(data, f)


