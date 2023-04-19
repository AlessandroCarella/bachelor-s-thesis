import json
import os
from os.path import join, isdir, isfile, abspath, dirname, normpath
import subprocess

import cv2
from feat import Detector
import torch

def getFPS (videoPath):
    cap = cv2.VideoCapture(videoPath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps

def findVideoFiles(path):
    mp4_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp4") or file.endswith(".avi"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

def getDetector ():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return Detector(
        face_model="retinaface",
        landmark_model="mobilefacenet",
        au_model="xgb",
        emotion_model="resmasknet",
        facepose_model="img2pose",
        device=device,
    )

def getFirstAnalysisFromVideo ():
    detector = getDetector ()

    datasetPath = abspath ("datasets/DAiSEE/")

    videosPaths = findVideoFiles(datasetPath)
    videoFPSs = []


    with open (join(abspath("src/analysis"), "video first analysis.json"), "w") as f:
            f.write ("[")

    for videoPath in videosPaths:
        video_prediction = (detector.detect_video(videoPath, skip_frames=getFPS (videoPath)))
        try:
            with open (join(abspath("src/analysis"), "video first analysis.json"), "a") as f:
                f.write (video_prediction.to_json ())
                f.write (",")
        except Exception as e:
            print ("----------------------------------ERRORE------------------------------------------------")
            print (videoPath)
            print (e)

    with open (join(abspath("src/analysis"), "video first analysis.json"), "a") as f:
        f.write ("]")

