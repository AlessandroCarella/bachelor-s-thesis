from os.path import join, isfile, abspath, dirname, exists, basename, splitext
import os
import torch
from feat import Detector
import pickle
import pandas as pd
from tqdm import tqdm

from mainUtility import makeAndSavePredictionsOnFile, getDetector, checkIfDirExistsAndIfNotCreateIt, readPredictionsListFromFile
from alternativeGetSingleVideoExtraction import getSingleVideoExtraction


def getVideoPaths () -> list[str]:
    with open (join(dirname(abspath(__file__)), "pathsAndLabels.pickle"), "rb") as f:
        videoPathsAndLabel = pickle.load (f)
    
    return list(videoPathsAndLabel.keys())

def getLabels () -> list[str]:
    with open (join(dirname(abspath(__file__)), "pathsAndLabels.pickle"), "rb") as f:
        videoPathsAndLabel = pickle.load (f)
    
    return list(videoPathsAndLabel.values())

def main ():
    ACTION_UNITS_THRESHOLD = 0.5

    if not exists((join(dirname(abspath(__file__)), "predictions.json"))):
        videosPath = getVideoPaths ()
        makeAndSavePredictionsOnFile (videosPath, getDetector())
    #predictions are saved on json file if they don't already exists
    data = readPredictionsListFromFile() 

    dirName = join(dirname(abspath(__file__)), "extractions")
    checkIfDirExistsAndIfNotCreateIt (dirName)
    i = 0
    for singleVideoData in tqdm(data): #itero sui video
        videoExtractions = getSingleVideoExtraction(singleVideoData, singleVideoData["label"], ACTION_UNITS_THRESHOLD)
        i += 1
        
        inputFile = splitext(basename(next(iter(videoExtractions.keys()))))[0]
        extraction = videoExtractions[inputFile]
        fileName = join (dirName, singleVideoData["label"], inputFile)
        with open (fileName + ".txt", "w") as f:
            for line in extraction:
                f.write (line + "\n")

main ()