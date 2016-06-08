import os

PARENT_DIR = os.path.dirname(os.path.realpath(__file__))



def main(object):
	extension = ".mp4"
	print "Starting..."

	for dirname, dirnames, filenames in os.walk(PARENT_DIR + "/clip/"):
		for filename in filenames:
			if filename.endswith(extension):

				filename = os.path.splitext(filename)[0]
				clipToBeRemoved = (PARENT_DIR + "/clip/" + filename + ".mp4")
				thumbToBeRemoved = (PARENT_DIR + "/thumb/"+ filename +  ".jpg")
				gpsToBeRemoved = (PARENT_DIR + "/gps/" + filename +  ".json")
				print "Deleting " + str(clipToBeRemoved)
				print ("DELETE " + str(clipToBeRemoved) + "\n")

				os.remove(clipToBeRemoved)
				os.remove(thumbToBeRemoved)
				os.remove(gpsToBeRemoved)

	print "Done..."

if __name__ == '__main__':
	main()
