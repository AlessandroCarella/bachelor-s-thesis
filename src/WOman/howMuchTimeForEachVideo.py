import time
import cv2

from mainUtility import getDetector

def getFrameCount(videoPath):
    cap = cv2.VideoCapture(videoPath)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count

firstVideoPath = r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\datasets\DAiSEE\DataSet\Test\500044\5000441002\5000441002.avi"
videoPath = r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\datasets\DAiSEE\DataSet\Test\500044\5000441001\5000441001.avi"

detector = getDetector()
startTime = time.time ()
detection = detector.detect_video(videoPath)
endtime = time.time ()

print ("time for each detection")
print (endtime-startTime)
print ("number of frames in the video")
print (getFrameCount (videoPath))