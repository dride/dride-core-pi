import cv2
from classes import frameAnalyzer


from matplotlib import pyplot as plt


# load the image
image = cv2.imread('/Users/saoron/cardiganCam/training/set5/frame1730.jpg')

frameAnalyzer.analyze_frame(image, False)

