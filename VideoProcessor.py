import cv2 as cv
from LaneMarkersModel import LaneMarkersModel
from LaneMarkersModel import normalize
import numpy as np
from Sensor import LaneSensor
from LineDetector import LineDetector

#Initialize video input
#stream = cv.VideoCapture(0) #6 7 8
stream = cv.VideoCapture("/Users/saoron/Desktop/driveRaw/encoded/1459324516.h264.mp4") #6 7 8
if stream.isOpened() == False:
    print "Cannot open input video"
    exit()

#Initialize video writing
# videoWriter = cv.VideoWriter('out7Test1.avi', cv.cv.CV_FOURCC('M','J','P','G'), 30, (640, 480), 1)

#some image processing parameters
cropArea = [50, 100, 500, 300]  #1 3 0 2
sensorsNumber = 100
sensorsWidth = 30

l_to = (35, 190)
l_from = (20, 100)
r_from = (360, 190)
r_to = (350, 100)


#6L
line1LStart = np.array(l_from)
line1LEnd = np.array(l_to)
#6R
line1RStart = np.array(r_from)
line1REnd = np.array(r_to)



#7L
#line1LStart = np.array([71, 163])
#line1LEnd= np.array([303, 3])

#get first frame for color model
flag, imgFull = stream.read()


imgFull = cv.flip(imgFull, -1)
imgFull = cv.flip(imgFull, 1)
img = imgFull[cropArea[1]:cropArea[3], cropArea[0]:cropArea[2]]

#Initialize left lane
leftLineColorModel = LaneMarkersModel()
#leftLineColorModel.InitializeFromImage(np.float32(img)/255.0, "Select left line")
leftLine = LineDetector(cropArea, sensorsNumber, sensorsWidth, line1LStart, line1LEnd, leftLineColorModel)

#Initialize right lane
rightLineColorModel = LaneMarkersModel()
#rightLineColorModel.InitializeFromImage(np.float32(img)/255.0, "Select right line")
rightLine = LineDetector(cropArea, sensorsNumber, sensorsWidth, line1RStart, line1REnd, rightLineColorModel)

frameNumber = 0
while(cv.waitKey(1) != 27):
    frameNumber+=1
    print frameNumber
    #read and crop
    flag, imgFull = stream.read()

    cv.circle(imgFull, l_from, 2, 255, -1)
    cv.circle(imgFull, l_to, 2, 255, -1)

    cv.circle(imgFull, r_from, 2, 255, -1)
    cv.circle(imgFull, r_to, 2, 255, -1)


    imgFull = cv.flip(imgFull, -1)
    imgFull = cv.flip(imgFull, 1)


    if flag == False: break #end of video

    #do some preprocessing to share results later
    img = np.float32(imgFull[cropArea[1]:cropArea[3], cropArea[0]:cropArea[2]])/255.0
    hsv = np.float32(cv.cvtColor(img, cv.COLOR_RGB2HSV))
    canny = cv.Canny(cv.cvtColor(np.uint8(img*255), cv.COLOR_RGB2GRAY), 70, 170)

    #make output images
    outputImg = img.copy()
    outputFull = imgFull.copy()

    #process frame
    leftLine.ProcessFrame(img, hsv, canny, outputImg, outputFull)
    rightLine.ProcessFrame(img, hsv, canny, outputImg, outputFull)

    #show output
    cv.imshow("Output", outputImg)
    cv.imshow("Output full", outputFull)
    
    #write output
    # videoWriter.write(outputFull)
    
cv.destroyAllWindows()