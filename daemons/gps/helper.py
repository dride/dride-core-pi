import json
import sys

from os import path
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

from classes.gps import GPS
from config import *


def run_program():

    position = {}

    # get speed from GPS
    position = GPS.getPosSerial()

    text_file = open(PARENT_DIR + "/daemons/gps/position", "w")
    text_file.write(position)
    text_file.close()

if __name__ == '__main__':
    while True:
        run_program()
