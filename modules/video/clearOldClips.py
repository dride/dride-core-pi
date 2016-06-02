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
    print "Starting..."
    while True:
		folderSizeBytes = getFolderSize(PARENT_DIR + "/clip/")
		print "Folder size:\t" + str(folderSizeBytes)
		print "Threshold size:\t" + str(2520435800)
		#8GB 8589934592
		#500mb 524288000
		if (folderSizeBytes >= 2520435800):
			clipToBeRemoved = oldest_file_in_tree(PARENT_DIR + "/clip/", ".mp4")
			thumbToBeRemoved = oldest_file_in_tree(PARENT_DIR + "/thumb/", ".jpg")
			gpsToBeRemoved = oldest_file_in_tree(PARENT_DIR + "/gps/", ".json")
			print "Deleting " + str(clipToBeRemoved)
			print ("DELETE " + str(clipToBeRemoved) + "\n")

			os.remove(clipToBeRemoved)
			os.remove(thumbToBeRemoved)
			os.remove(gpsToBeRemoved)
		else:
			print ("No files to be deleted, folder size "+ str(folderSizeBytes) +"\n")
			print "Sleeping"
			time.sleep(60 * 10)

if __name__ == '__main__':
	main()
