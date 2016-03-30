'''
Created on Nov 27, 2011

@author: Dima
'''

import cv2 as cv
import numpy as np

class LaneSensor():
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
        self.width = 0
        self.lineRGB = [0, 0, 0]
        self.lineHSV = [0, 0, 0]
        self.lineWidth = [0, 0]
        self.roadRGB = [0, 0, 0]
        self.roadHSV = [0, 0, 0]

    def SetGeometry(self, position, width):
        self.xPos = max(0, position[0]-width/2)
        self.yPos = position[1] 
        self.width = width

    def DrawGeometry(self, img):
        cv.line(img, (self.xPos, self.yPos), (self.xPos+self.width, self.yPos), [0, 0, 255])
    
    def InitializeModel(self, linergb, linehsv, roadrgb, roadhsv):
        self.lineRGB = linergb
        self.lineHSV = linehsv
        self.roadRGB = roadrgb
        self.roadHSV = roadhsv

    def CalculatePixelsProperties(self, rgb, hsv):
        #simple RGB distance
        rgbLaneError = np.abs(rgb - self.lineRGB)
        rgbLaneDistance = np.sqrt(np.square(rgbLaneError[:,0])+np.square(rgbLaneError[:,1])+np.square(rgbLaneError[:,2]))/3.0

        HLaneError = np.abs(hsv - self.lineHSV)[:, 0]/360.0
        
        #reliability is 1 for now
        probability = 1.0-(1.0*rgbLaneDistance + 0.0*HLaneError)/1.0
        reliability = np.ones_like(probability)
        
        return (probability, reliability)
       
    def FindSegments(self, rgbGlobal, hsvGlobal, cannyGlobal, outputImg, previousLineCenterPosition):
        #crop image to a sensor size
        rgb = rgbGlobal[self.yPos, self.xPos:(self.xPos+self.width)]
        hsv = hsvGlobal[self.yPos, self.xPos:(self.xPos+self.width)]
        canny = cannyGlobal[self.yPos, self.xPos:(self.xPos+self.width)]

        probability, reliability = self.CalculatePixelsProperties(rgb, hsv)

        #check if we have any data
        if canny.shape[0] == 0: return [0, [], []]

        #find start of a first segment
        segStart = 0
        while canny[segStart] == 0: #find start of a first segment
            segStart+=1 
            if segStart == canny.shape[0]:
                break
            
        #find Canny segments
        segments = []
        segmentProbability = 0
        for x in range(1, canny.shape[0]):
            if canny[x] > 0 and (x - segStart) > 2: #skip segments which have less than 2 pixels including 1 edge
                segmentProbability = np.average(probability[segStart:x])
                segments.append([segStart, x, segmentProbability])
                segStart = x
        
        #find line segments
        lineSegments = []
        for seg in segments:
            segmentProbability = seg[2]
            #just check color
            if segmentProbability > 0.85:
                segmentProbability = 1
            else:
                segmentProbability = 0
            
            #check line width
            if self.lineWidth[1] > 10: 
                if abs((seg[1]-seg[0])-self.lineWidth[0]/self.lineWidth[1]) > 5+50/self.lineWidth[1]:
                    segmentProbability = 0
                    
            cv.line(outputImg, (self.xPos+seg[0], self.yPos), (self.xPos+seg[1], self.yPos), [segmentProbability, segmentProbability, 0], 1)
            if(segmentProbability == 1):
                lineSegments.append([self.xPos+seg[0], self.xPos+seg[1]])
        
        lineCenter = previousLineCenterPosition-self.xPos
        if len(lineSegments) == 0 and len(segments) >= 3: #we have not found any line segments but we still have some segments 
            #lets try to recover and update the model if we have a segment which looks good
            for seg in segments:
                if(seg[0] <= lineCenter and seg[1] >= lineCenter and self.lineWidth[1] > 10): #maybe it's actually a line...
                    if abs((seg[1]-seg[0])-self.lineWidth[0]/self.lineWidth[1]) < 10:
                        lineSegments.append([self.xPos+seg[0], self.xPos+seg[1]])
        
        return (len(lineSegments), lineSegments, segments)

    def UpdatePositionAndModelFromRegion(self, rgbGlobal, hsvGlobal, region):
        x1 = region[0]
        x2 = region[1]
        self.xPos = max(0, x1 - (self.width - (x2-x1))/2)
        rgb = rgbGlobal[self.yPos, x1:x2]
        hsv = hsvGlobal[self.yPos, x1:x2]
        self.lineRGB = [np.average(rgb[:, 0]), np.average(rgb[:, 1]), np.average(rgb[:, 2])]
        self.lineHSV = [np.average(hsv[:, 0]), np.average(hsv[:, 1]), np.average(hsv[:, 2])]
        self.lineWidth[0]+= x2-x1 
        self.lineWidth[1]+= 1 
        
    def UpdatePositionIfItIsFarAway(self, previousLineCenterPosition):
        if abs(previousLineCenterPosition - self.xPos+self.width/2) > 20:
            self.xPos = int(max(0, previousLineCenterPosition - self.width/2))
        
#TEST        
    def UpdatePositionBasedOnCanny(self, cannyGlobal):
        canny = cannyGlobal[self.yPos, :]
        xr=self.xPos+self.width/2
        while (xr<canny.shape[0] and canny[xr]==0): xr+=1
        xl=self.xPos+self.width/2
        while (xl>0 and canny[xl]==0): xl-=1
        self.xPos = (xl+xr)/2-self.width/2
