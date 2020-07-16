# fluidity-test
Simple OpenCV based fluidity testing tool

### Problem

When developing apps is nice to know the fluidity of animations and page transitions, but the tools between Android and iOS can get a bit unweildy.

### Solution
As a lunchtime project I hacked some of my bee detection code to create a fluidity tool.  Input video is just a screen recording from a phone. Output video shows a count of 'static screens' i.e. how many frames have not change, as well as real time fluidity fps, which is calculated as

    fluidity fps = video framerate /  staticScreens  
    
These are overlaid to the original video so you can see ‘animations of interest’, or scroll through the output to whatever you wanted to examine.

### Setup
Install opencv on your system, e.g. for MacOS

`brew install opencv`

### Usage

Run the python script with the video you want to analyze

`python3 fluidity.py RPReplay_Final1594317061.mp4`


### References
Lambda/AWS deployment greatly assisted by this:
https://itnext.io/create-a-highly-scalable-image-processing-service-on-aws-lambda-and-api-gateway-in-10-minutes-7cbb2893a479
