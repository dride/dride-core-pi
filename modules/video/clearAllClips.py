import os
import time
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def oldest_file_in_tree(rootfolder, extension=".mp4"):

    _min = None
    for dirname, dirnames, filenames in os.walk(rootfolder):
        for filename in filenames:
          if filename.endswith(extension):
            if (filename) < _min or _min is None:
				_min = filename

    return rootfolder + str(_min)

def main():
	extension = ".mp4"
	print "Starting..."

	for dirname, dirnames, filenames in os.walk(PARENT_DIR + "/clip/"):
		for filename in filenames:
			if filename.endswith(extension):
				filename = os.path.splitext(filename)[0]
				clipToBeRemoved = (PARENT_DIR + "/clip/" + filename + ".mp4")
				thumbToBeRemoved = oldest_file_in_tree(PARENT_DIR + "/thumb/"+ filename +  ".jpg")
				gpsToBeRemoved = oldest_file_in_tree(PARENT_DIR + "/gps/" + filename +  ".json")
				print "Deleting " + str(clipToBeRemoved)
				print ("DELETE " + str(clipToBeRemoved) + "\n")

				os.remove(clipToBeRemoved)
				os.remove(thumbToBeRemoved)
				os.remove(gpsToBeRemoved)


if __name__ == '__main__':
	main()
