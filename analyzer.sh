# Shell script to encapsulate python for video analyzer
# Author: Kelton Temby
# Date 2020
# 
# Inputs 
videoForProcessing=$1
processedVideo=$2

# Assert we have opencv installed
if ! python3 -c 'import cv2; print(cv2.__version__)'; then
    echo Python error - please ensure python and opencv are installed
    exit
fi

# Assert we have ffmpeg installed
if ! ffmpeg -version | sed -n "s/ffmpeg version \([^ ]*\).*/\1/p;"; then
    echo Python error - please ensure python and opencv are installed
    exit
fi

# Process the video
python3 fluidity.py $videoForProcessing

# Compress the result
ffmpeg -i AlgVideo.mp4 -c:v libx264 -preset slow -crf 22 -c:a copy $processedVideo
