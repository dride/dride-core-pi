import cv2
import numpy as np
import time
from config import *
from classes.gps import GPS


class capture:

	# load config
	config = Config().getConfig()

	rolloverMinutes = 1
	rollover = rolloverMinutes * 60
	camera  = None
	shutdownRequest = False
	parent = PARENT_DIR + '/modules/video/'
	out = None
	# Define the codec
	# TODO : inject codec by OS
	fourcc = cv2.VideoWriter_fourcc(*'X264')
	timestamp = int(round(time.time()))
	lastRollover = 0
	gps = GPS()
	filename = '';

	def __init__(self, w, h):

		self.w = w
		self.h = h

	def captureFrame(self, frame):

		# if we dont have any video object or we need to replace file due to size limit
		if self.out is None or (self.timestamp != self.lastRollover and (self.timestamp % self.rollover) == 0):

			# Release everything if job is finished
			if self.out is not None:
				self.out.release()

			# save current timestamp
			self.timestamp = int(round(time.time()))
			self.lastRollover = self.timestamp
			self.lastRollover = self.timestamp

			self.filename = str(self.timestamp)

			# save thumbnail
			cv2.imwrite(self.parent + "thumb/" + self.filename + ".jpg", frame)

			# create GPS file
			if self.config['gps'] == True:
				self.gps.createNewGPSrecordFile(self.filename)

			# Create new VideoWriter object
			self.out = cv2.VideoWriter(self.parent + "clip/" + self.filename + ".mp4", self.fourcc, 20, (self.w, self.h))


		if self.config['gps']==True:
			# save GPS data for frame
			self.gps.AppendGPSPositionToCurrentFile(self.filename)

		# add waterMark
		# read images
		mark = cv2.imread('assets/images/watermark.png')
		m, n = frame.shape[:2]
		# create overlay image with mark at the upper left corner, use uint16 to hold sum
		overlay = np.zeros_like(frame, "uint16")
		overlay[:mark.shape[0], :mark.shape[1]] = mark
		# add the images and clip (to avoid uint8 wrapping)
		frame = np.array(np.clip(frame + overlay, 0, 255), "uint8")

		# write the frame to video file
		self.out.write(frame)

		self.timestamp = int(round(time.time()))


	def free_space_up_to(free_bytes_required=10000000000, rootfolder="/clip/", filesize=104857600, basename="filename-"):
		# Deletes rootfolder/basename*, oldest first, until there are free_bytes_required available on the partition.
		# Assumes that all files have file_size, and are all named basename{0,1,2,3,...}
		# Returns number of deleted files.
		statv = os.statvfs(rootfolder)
		required_space = free_bytes_required - statv.f_bfree*statv.f_bsize
		basepath = os.path.join(rootfolder, basename)
		if required_space <= 0:
			return 0

		# "1 +" here for quickly rounding
		files_to_delete = 1 + required_space/filesize

		# List all matching files. If needed, replace with os.walk for recursively
		# searching into subdirectories of rootfolder
		file_list = [os.path.join(rootfolder, f) for f in os.listdir(rootfolder) if f.startswith(basename)]

		# Alternatively, if the filenames can't be trusted, sort based on modification time
		file_list.sort(key=lambda i: os.stat(i).st_mtime)

		for f in file_list[:files_to_delete]:
			print 'removed f'
			os.remove(f)
		return files_to_delete