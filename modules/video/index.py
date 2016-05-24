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
res = []

for file in files:
    if file != '.gitignore' and file !='.DS_Store':
        res.append(file.replace('.avi', ''))


print json.dumps(res, default=lambda o: o.__dict__)

