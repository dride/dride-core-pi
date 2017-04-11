from config import *
import json
import time
import serial

port = "/dev/ttyS0"    # Raspberry Pi 3

class GPS(object):

	@classmethod
	def getPos(self):

		position = {}

		ser = serial.Serial(port, baudrate = 9600, timeout = 1)
		latLon = [-1, -1];
		speed = 0;

		for row in range(0, 10):
		    data = ser.readline()
		    latLon = self.parseGPS(data) if self.parseGPS(data) != [-1, -1] else latLon
		    speed = self.parseSpeed(data) if self.parseSpeed(data)!= -1 else speed

		position["latitude"] = latLon[0]
		position["longitude"] = latLon[1]
		position["speed"] = speed
		# TODO
		position["heading"] = '-1'

		return json.dumps(position)


	#	Fast method to return current speed
	@classmethod
	def getSpeed(self):

		ser = serial.Serial(port, baudrate = 9600, timeout = 1)
		speed = 0;

		while True:
		    data = ser.readline()
		    speed = self.parseSpeed(data)
		    
		    if speed > -1:
		    	return self.parseSpeed(data)

		return 0


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


	@classmethod
	def parseGPS(self, data):
	    lat = lon = -1
	    if data[0:6] == "$GPGGA":
	        s = data.split(",")
	        if s[7] == '0':
	            print "no satellite data available"
	            return        
	        lat = self.decode(s[2], s[3])
	        lon = self.decode(s[4], s[5])

	    return [lat, lon]

	@classmethod
	def parseSpeed(self, data):
	#    print "raw:", data
	    speed = -1
	    if data[0:6] == "$GPRMC":
	        speedParse = data.split(",")
	        speed = speedParse[7]

	    return speed

	@classmethod
	def dms2dd(self, degrees, minutes, seconds, direction):
	    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
	    if direction == 'E' or direction == 'N':
	        dd *= -1
	    return dd;

	@classmethod
	def decode(self, coord, direction):
	    # DDDMM.MMMMM -> DD deg MM.MMMMM min
	    v = coord.split(".")
	    head = v[0]
	    tail =  v[1]
	    deg = head[0:-2]
	    min = head[-2:]
	    return self.dms2dd(deg, min, "0." + tail, direction)

