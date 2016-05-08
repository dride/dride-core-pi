

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
Y1 = 240  # 4.5.16 ->200
X1 = 200

ROAD_HEIGHT = 120
ROAD_WIDTH = 300