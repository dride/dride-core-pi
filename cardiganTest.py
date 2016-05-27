import random
import unittest
import sys

sys.path.insert(0,'/usr/lib/pyshared/python2.7')

import cv2
import numpy as np


"""Simple test harness"""
class TestImages(unittest.TestCase):

    def test_white(self):
        self.assertTrue((cv2.imread("training/set6/1.png").any()))




if __name__ == '__main__':
    unittest.main()