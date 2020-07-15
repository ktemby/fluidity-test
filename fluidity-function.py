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
    self.cam=cv2.VideoCapture(fileName)

    self.videoWidth=int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    self.videoHeight=int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    self.videoFramerate=int(cam.get(cv2.CAP_PROP_FPS))

    print(f"Base video framerate: {videoFramerate}")

    # Define the codec and create VideoWriter object
    self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    self.video = cv2.VideoWriter(outputFile,fourcc,videoFramerate,(videoWidth,videoHeight))

    # Parameters 
    self.maxFrame = videoFramerate*10 # let it analze just 10 seconds
    self.minFrame = 1
    self.binaryThresh = 10

    # UI Parameters
    dfont=cv2.FONT_HERSHEY_DUPLEX
    fontColor=(0,0,255,255)

    # Calculate differential image
    def diffImg(t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)

    def fluidity(videoFramerate, framesSinceChange):
        # E.g. 2 frames since change, framerate 60 -> 60/2 = 30 fps
        fps = int(videoFramerate/(framesSinceChange))
        return fps 

    def analyze(self):
        framesSinceChange = 1
        frame = 0
        while frame < self.minFrame:
            s, img = cam.read()
            frame +=1
            if not s:
                break

        # Read three images first:
        s, img = cam.read()
        t_minus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

        # Loop through all frames in video
            while f < self.maxFrame:
                
                # Read next image
                prev = img
                s, img = cam.read()
                if not s:
                    break	

                # Shift the frames under analysis
                t_minus = t
                t = t_plus
                t_plus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                f = f+1 # keep track of frame number

                dfI=diffImg(t_minus,t,t_plus) # Differential impage
                rt, gb=cv2.threshold(dfI,binaryThresh,255,cv2.THRESH_BINARY) # Threshold to clear noisy noise
                contours,hierarchy = cv2.findContours(gb,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # simple contour detect

                # Did the image change?
                if contours:
                    framesSinceChange = 1
                else:
                    framesSinceChange += 1

                currentFluidity = fluidity(videoFramerate, framesSinceChange) # Get the real time fluidity 

                # Show the feed (will turn this off for headless mode)
                cv2.putText(prev, format(f"Static Frames: {framesSinceChange}"), (50,50),dfont,2,fontColor)
                cv2.putText(prev, format(f"Fluidity: {currentFluidity} fps"),(50,150),dfont,2,fontColor)
                cv2.drawContours(prev, contours,-1,(0,0,255),1)
                self.video.write(prev)

        self.video.release()
        self.cam.release()
        return outputFile
        
if __name__ == '__main__':
    fluidity = FluidityAnalyzer(sys.argv[1], sys.argv[2])
    success = fluidity.analyze()
    print(f"Analysis completed: {success}")
