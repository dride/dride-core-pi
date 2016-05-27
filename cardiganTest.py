import random
import unittest
import sys

sys.path.insert(0,'/usr/lib/pyshared/python2.7')

import cv2
import numpy as np
from classes import frameAnalyzer
from config import *

"""Simple test harness"""
class TestImages(unittest.TestCase):


    def test_image_load(self):
        self.assertTrue((cv2.imread("training/set6/1.png").any()))


    def test_lane_detection(self):
        # load config for test
        # TODO: create a way to load different config files in testing.

        image = cv2.imread('training/set6/1.png')
        f = frameAnalyzer.analyze_frame(image, True, False, True)
        self.assertTrue(f.laneAvg == 170)


if __name__ == '__main__':
    unittest.main()