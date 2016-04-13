class frameMemory:

	frames = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]

	def __init__(self, size):
		self.size = size  # instance variable unique to each instance


	def put(self, num, frameNum):
		frameToReplace = self.get_next_slot()
		for x in range(0, 6):
			if self.frames[x][1] == frameToReplace:
				self.frames[x][0] = num
				self.frames[x][1] = frameNum


	def getSum(self):
		sum = 0
		for x in range(0, self.size):
			sum += self.frames[x][0]

		return sum

	def get_next_slot(self):
		# assume first node is the minimum
		min = self.frames[0][1]
		for x in range(0, 6):
			if (self.frames[x][1] < min):
				min = self.frames[x][1]
		# return frame number of minimum value
		return min

	def toString(self):

		print self.frames