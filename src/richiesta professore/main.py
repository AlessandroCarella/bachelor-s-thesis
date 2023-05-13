from os.path import join, isfile, abspath, dirname, exists
import os
import torch
from feat import Detector
import pickle
import pandas as pd
from tqdm import tqdm

from getPredictionsAndSaveThemOnFile import getPredictionsAndSaveThemOnFile, readPredictionsListFromFile
from getSingleVideoExtraction import getSingleVideoExtraction

def buildNewDetector (filePathDetector:str) -> Detector:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #device = "cpu"
    detector = Detector(
        face_model="retinaface",
        landmark_model="mobilefacenet",
        au_model="xgb",
        emotion_model="resmasknet",
        facepose_model="img2pose",
        device=device,
    )
    
    with open (filePathDetector, "wb") as f:
        pickle.dump (detector, f)

    return detector

def getDetector () -> Detector:
    filePathDetector = join(dirname(abspath(__file__)), "detector.pickle")
    if isfile (filePathDetector):
        with open (filePathDetector, "rb") as f:
            detector = pickle.load (f)
        if detector.device == "cuda" and not torch.cuda.is_available():
            detector = buildNewDetector (filePathDetector)
    else:
        detector = buildNewDetector (filePathDetector)

    return detector

def getVideoPaths () -> list[str]:
    #path al primo video nel dataset
    #test
    #return ["C:/Users/Alessandro/Pictures/Camera Roll/WIN_20230513_17_16_31_Pro.mp4"]
    return [
        #drowsy e looking away sono presenti solo nell'altro dataset che non ha video ma immagini
        #enaged
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/928901/9289010216/9289010216.avi")),
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/500067/5000672074/5000672074.avi")),
        #bored
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/510035/5100352054/5100352054.avi")),
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/826412/8264120121/8264120121.avi")),
        #confused
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/510009/5100091062/5100091062.avi")),
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/987736/987736015/987736015.avi")),
        #frustated
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/510038/5100381069/5100381069.avi")),
        (join(dirname(abspath(__file__)), "../datasets/DAiSEE/DataSet/Test/928901/9289010113/9289010113.avi"))
    ]

def getDAiSEEdatasetCleanedOnlyInputAndLabel() -> pd.DataFrame:
    DAiSEE = pd.read_csv ((join(dirname(abspath(__file__)), "../final analysis/DAiSEE and student engagement dataset clean.csv")))
    return DAiSEE[['input', 'label']]

def checkIfDirExistsAndIfNotCreateIt (dirPath:str) -> None:
    if not exists (dirPath):
        os.makedirs(dirPath)

if __name__ == "__main__":
    ACTION_UNITS_THRESHOLD = 0.5

    videosPathMain = getVideoPaths ()

    #data = getPredictionsAndSaveThemOnFile (videosPathMain, getDetector())
    #le predizioni effettuate vengono salvate su file json, quindi, 
    #se si necessita di effettuare l'estrazione di nuovo, è
    #possibile farlo attraverso il seguente metodo
    data = readPredictionsListFromFile() 
    
    DAiSEE = getDAiSEEdatasetCleanedOnlyInputAndLabel()

    videoExtractions = []
    for singleVideoData in tqdm(data): #itero sui video
        videoExtractions.append(getSingleVideoExtraction(singleVideoData, DAiSEE, ACTION_UNITS_THRESHOLD))
    
    dirName = join(dirname(abspath(__file__)), "extractions")
    checkIfDirExistsAndIfNotCreateIt (dirName)
    for videoExtractions in videoExtractions:
        inputFile = next(iter(videoExtractions.keys()))
        extraction = videoExtractions[inputFile]
        fileName = join (dirName, inputFile)
        with open (fileName + ".txt", "w") as f:
            for line in extraction:
                f.write (line + "\n")
    

    