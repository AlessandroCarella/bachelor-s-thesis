from feat import Detector
import json

import os
from os.path import join, isdir, isfile, abspath, dirname

import torch


def saveAnalysisToFile (filePath, analysis):
    with open (filePath, "w") as file:
        file.write (json.dumps (analysis, indent=4))

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

def extractFeaturesFromImagesWithPyFeat ():
    detector = getDetector()


    allFoldersWithImagesPathsAndRelativeImagesPaths = {}
    with open (join(abspath ("src"), "allFoldersWithImagesPathsAndRelativeImagesPaths.json"), "r") as f:
        allFoldersWithImagesPathsAndRelativeImagesPaths = json.load(f)

    for key, value in allFoldersWithImagesPathsAndRelativeImagesPaths.items():
        filePath = join (key, "analysis.json")
        singleKeyAnalysis = []
        for img in value:
            imagePath = join(key, img)
            imgAnalysis = detector.detect_image(imagePath).to_json()
            singleKeyAnalysis.append(imgAnalysis)
            saveAnalysisToFile (filePath, singleKeyAnalysis)

