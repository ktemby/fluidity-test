# /usr/bin/python\
# Python to count and display the average number of objects per second moving in a video
# Assumption shown in parameters
# @Author: Kelton Temby 2014
# Copyright Keltronix 2014
# 
# Simple opencv tool to quantify fluidity
#
# Input: a recorded video
# Output: a side-by-side video showing framerate
#
# Do simple frame subtraction 
#
# visualize framerate
# visualize framerate between last different frame

import cv2
import time
import sys

class FluidityAnalyzer:
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        
        # Create capture device
        self.cam=cv2.VideoCapture(self.inputFile)

        videoWidth=int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoHeight=int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.videoFramerate=int(self.cam.get(cv2.CAP_PROP_FPS))
        print(f"Base video framerate: {self.videoFramerate}")

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video = cv2.VideoWriter(self.outputFile,fourcc,self.videoFramerate,(videoWidth,videoHeight)) 
        
        # Parameters 
        self.maxFrame = self.videoFramerate*10 # let it analze just 10 seconds
        self.minFrame = 1
        self.binaryThresh = 10

        # UI Parameters
        self.dfont=cv2.FONT_HERSHEY_DUPLEX
        self.fontColor=(0,0,255,255)

    # Calculate differential image
    def diffImg(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)

    def fluidity(self, videoFramerate, framesSinceChange):
        # E.g. 2 frames since change, framerate 60 -> 60/2 = 30 fps
        fps = int(videoFramerate/(framesSinceChange))
        return fps 

    def analyze(self):
        framesSinceChange = 1
        frame = 0
        while frame < self.minFrame:
            s, img = self.cam.read()
            frame +=1
            if not s:
                break

        # Read three images first:
        s, img = self.cam.read()
        t_minus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)

        # Loop through all frames in video
        while frame < self.maxFrame:
            
            # Read next image
            prev = img
            s, img = self.cam.read()
            if not s:
                break	

            # Shift the frames under analysis
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            frame += 1 # keep track of frame number
            
            dfI=self.diffImg(t_minus,t,t_plus) # Differential impage
            rt, gb=cv2.threshold(dfI,self.binaryThresh,255,cv2.THRESH_BINARY) # Threshold to clear noisy noise
            contours,hierarchy = cv2.findContours(gb,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # simple contour detect

            # Did the image change?
            if contours:
                framesSinceChange = 1
            else:
                framesSinceChange += 1
    
            currentFluidity = self.fluidity(self.videoFramerate, framesSinceChange) # Get the real time fluidity 

            # Visualize the result
            cv2.putText(prev, format(f"Static Frames: {framesSinceChange}"), (50,50),self.dfont,2,self.fontColor)
            cv2.putText(prev, format(f"Fluidity: {currentFluidity} fps"),(50,150),self.dfont,2,self.fontColor)
            cv2.drawContours(prev, contours,-1,(0,0,255),1)
            self.video.write(prev)

        self.video.release()
        self.cam.release()
        print(f"Analysis completed on {self.outputFile}")
        
if __name__ == '__main__':
    fluidity = FluidityAnalyzer(sys.argv[1], sys.argv[2])
    success = fluidity.analyze()
    print(f"Analysis completed: {success}")
