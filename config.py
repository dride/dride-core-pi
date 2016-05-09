

# mode
# 0 - from video file
# 1 - from raspberry piCamera
INPUT_TYPE = 0


#project dir
PARENT_DIR = '/Users/saoron/cardiganCam/' if INPUT_TYPE == 0 else  '/home/cardiganCamVision/'


# picture calibration

# FPS
FPS = 8
# X value of avg center of lane
LANE_CENTER = 100

# Left upper point of road window
Y1 = 170  # 4.5.16 ->200
X1 = 150

ROAD_HEIGHT = 250
ROAD_WIDTH = 300
# delta for where to find cars square
deltaX = 160
deltaY = -70
SQUARE_WIDTH = 160