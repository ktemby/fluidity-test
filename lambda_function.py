import json
import cv2
import fluidityAnalyzer
import base64
   
def write_to_file(save_path, data):
    with open(save_path, "wb") as f:
      f.write(base64.b64decode(data))
   
def lambda_handler(event, context):
    inFile = "/tmp/videoFile.mp4"
    outFile = "/tmp/outputFile.mp4"
    
    # Write request body data into file
    write_to_file(inFile, event["body"])
    
    analyzer = fluidityAnalyzer.FluidityAnalyzer(inFile, outFile)
    analyzer.analyze()
    
    # Convert videoOutput to base64
    with open(outFile, "rb") as vid:
      str = base64.b64encode(vid.read())
      encoded_vid = str.decode("utf-8")
    
    # Return the data to API Gateway in base64.
    # API Gateway will handle the conversion back to binary.
    return {
      "isBase64Encoded": True,
      "statusCode": 200,
      "headers": { "content-type": "video/mp4"},
      "body":  encoded_vid
    }
