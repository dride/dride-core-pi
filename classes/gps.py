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

	# This method will update the transit file with the GPS object
	# Can be used for debug and for getting GPS from hardware
	# Another way to update this file is therw a GET request to : /modules/setGPS/?data=_GPS JSON_
	def updateSystemPositionData(self, time, filename):

		posObj = self.getPositionObjectByTime(time, filename)
		if posObj and posObj is not None:
			with open(PARENT_DIR + "/modules/gps/gps.json", 'w') as f:
				json.dump(posObj, f)

	@classmethod
	def getPositionObjectByTime(self, time, filename):
		print 'look for ' + str(int(filename) + int(time)) + ' in ' + filename  +'.json'
		_file = open(PARENT_DIR + "/training/wGPS/gps/"+filename+".json", 'r')
		frames = json.loads(_file.read())
		try:
			res = frames[str(int(filename) + int(time))]
			return res
		except KeyError:
			return None

		# res = None
		# for (i, element) in enumerate(frames):
		# 	# print str(int(element) - int(filename) + int(time)) + '   ' + element
		# 	# print int(element)
		# 	# print int(filename) + int(time)
		# 	# print int(element) < int(int(filename) + int(time))
		# 	# print
		# 	if int(element) < int(filename) + int(time):
		# 		res = (frames[element])
		# 	else:
		# 		print res
		# 		return res

		#
		# print
		# print