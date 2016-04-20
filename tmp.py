import cv2
import numpy as np
cam= cv2.VideoCapture("/Users/saoron/Desktop/driveRaw5/encoded/1460634130.h264.mp4")
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
while(cam.isOpened):
   f,img=cam.read()
   if f==True:
       img=cv2.flip(img,1)
       img=cv2.flip(img,-1)
       img=cv2.medianBlur(img,3)

       sigma = 0.33
       v = np.median(img)
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

       # apply automatic Canny edge detection using the computed median
       lower = int(max(0, (1.0 - sigma) * v))
       upper = int(min(255, (1.0 + sigma) * v))
       edged = cv2.Canny(gray, lower, upper)


       fgmask = fgbg.apply(edged)
       cv2.imshow('track',fgmask)
       cv2.imshow('track2',img)
       cv2.imshow('track3',edged)
   if(cv2.waitKey(27)!=-1):
       cam.release()
       cv2.destroyAllWindows()
       #break