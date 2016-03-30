'''
Created on Nov 26, 2011

@author: Dima
'''
import cv2 as cv
import numpy as np

def normalize(a):
    return (a-np.min(a))/(np.max(a)-np.min(a))

class LaneMarkersModel():
    def __init__(self):
        self.avgRGB = [ 0.8888889,   0.99607843,  0.98823529 ]
        self.avgHSV = [ 1.75261841e+02,   1.07563006e-01,   9.96078432e-01 ]
        self.lineProbabilityMap = 0
        self.initialPoints = []

    def UpdateModelFromMask(self, mask, img, hsv):
        self.avgRGB = cv.mean(img, mask)[0:3]
        self.avgHSV = cv.mean(hsv, mask)[0:3]
        distMap = cv.distanceTransform(1-mask, cv.cv.CV_DIST_L2, 5)[0]
        self.lineProbabilityMap = (1.0/(1.0+0.1*distMap))
        print self.avgRGB 
        print self.avgHSV 
        #cv.imshow('test',self.lineProbabilityMap)
        #cv.waitKey(1)
    
    def InitializeFromImage(self, img, windowName):
        cv.imshow(windowName, img)
        cv.setMouseCallback(windowName, self.AddPoint, [img, windowName])
        cv.waitKey(0)
        
        #calculate average lane color
        hsv = np.float32(cv.cvtColor(img, cv.COLOR_RGB2HSV))
        
        if len(self.initialPoints)>0:
            flooded = np.uint8(img*255)
            largeMask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
            largeMask[:] = 0
            lo = 20
            hi = 20
            flags = cv.FLOODFILL_FIXED_RANGE
            cv.floodFill(flooded, largeMask, (self.initialPoints[0][1], self.initialPoints[0][0]), (0, 255, 0), (lo,), (hi,), flags)
            mask = largeMask[1:largeMask.shape[0]-1, 1:largeMask.shape[1]-1]
            cv.imshow(windowName, mask*255)
            self.UpdateModelFromMask(mask, img, hsv)
        cv.destroyWindow(windowName)

    def AddPoint(self, event, x, y, flags, data):
        if event & cv.EVENT_LBUTTONUP:
            #print x, y, data[0][y, x]
            self.initialPoints.append([y, x])
            imgWithLines = data[0]
            '''
            if len(self.initialPoints)>1:
                cv.line(imgWithLines, (self.initialPoints[0][1], self.initialPoints[0][0]), (self.initialPoints[1][1], self.initialPoints[1][0]), [0,1,0], 2)
            if len(self.initialPoints)>3:
                cv.line(imgWithLines, (self.initialPoints[2][1], self.initialPoints[2][0]), (self.initialPoints[3][1], self.initialPoints[3][0]), [0,1,0], 2)
            '''
            flooded = np.uint8(imgWithLines*255)
            mask = np.zeros((imgWithLines.shape[0]+2, imgWithLines.shape[1]+2), np.uint8)
            mask[:] = 0
            lo = 20
            hi = 200
            flags = cv.FLOODFILL_FIXED_RANGE
            cv.floodFill(flooded, mask, (self.initialPoints[0][1], self.initialPoints[0][0]), (0, 255, 0), (lo,)*3, (hi,)*3, flags)
            cv.imshow(data[1], mask*255)
            
            

if __name__ == '__main__':
    img = cv.imread("C:\opencv\samples\cpp\lena.jpg")
    test = LaneMarkersModel()
    test.InitializeFromImage(np.float32(img)/255.0, 'test')
