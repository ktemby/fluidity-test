# fluidity-test
Simple OpenCV based fluidity testing tool

### Problem

When developing apps is nice to know the fluidity of animations and page transitions, but the tools between android and iOS can get a bit unweildy.

### Solution
As a lunchtime project I hacked some of the Eyesonhives code to create a fluidity tool.  Input video is just a screen recording from a phone, output video shows real time fluidity fps, overlaid to the original video so you can see ‘animations of interest’, or scroll through the output to whatever you wanted to examine.

### Setup
Install opencv on your system, e.g. for MacOS

`brew install opencv`

### Usage

Run the python script with the video you want to analyze

`python3 fluidity.py RPReplay_Final1594317061.mp4`
