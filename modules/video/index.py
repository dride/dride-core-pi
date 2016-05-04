########################################
#
# Return JSON with all the clips on disk
#
########################################


import json
from os import listdir
from os.path import isfile, join

# add file to index.json
jsonRaw = ''
path = "clip/"
files = [f for f in listdir(path) if isfile(join(path, f))]
c = 0
for file in files:
    files[c] = file.replace('.mp4', '')
    c+=1

print json.dumps(files, default=lambda o: o.__dict__)

