import unittest
import sys
from classes import frameAnalyzer
from config import *

sys.path.insert(0,'/usr/lib/pyshared/python2.7')
import cv2



class TestImages(unittest.TestCase):

    def test_image_load(self):
        self.assertTrue((cv2.imread(PARENT_DIR + "/training/set6/1.png").any()))

    def test_lane_detection(self):
        image = cv2.imread(PARENT_DIR + "/training/set6/1.png")
        f = frameAnalyzer.analyze_frame(image, True, False, True, False)

        self.assertTrue(f.laneAvg == 210)


if __name__ == '__main__':
    unittest.main()