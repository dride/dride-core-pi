import json
import sys

from os import path
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from classes.gps import GPS
from config import *

def clear_position():

    position = '{"latitude": -1, "speed": 0, "heading": "-1", "longitude": -1}'

    text_file = open(PARENT_DIR + "/daemons/gps/position", "w")
    text_file.write(position)
    text_file.close()


def run_program():

    position = {}

    # get speed from GPS
    position = GPS.getPosSerial()

    text_file = open(PARENT_DIR + "/daemons/gps/position", "w")
    text_file.write(position)
    text_file.close()

if __name__ == '__main__':
	
	# clear last know fix on startup
	clear_position()

    while True:
        run_program()
