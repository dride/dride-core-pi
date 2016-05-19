import os
from config import *

filename = '1'
file = open(PARENT_DIR + "/modules/video/gps/" + filename + ".json", 'r')
print file.read()
# file.write('Hello, world!\n')