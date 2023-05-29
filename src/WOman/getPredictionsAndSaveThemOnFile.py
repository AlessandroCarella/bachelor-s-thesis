from os.path import join, abspath, dirname
from feat import Detector
import pandas as pd
from tqdm import tqdm
import json

def openListOnFile ():
    with open ((join(dirname(abspath(__file__)), "predictions.json")), "w") as f:
        f.write("[\n")

def closeListOnFile ():
    with open ((join(dirname(abspath(__file__)), "predictions.json")), "a") as f:
        f.write("\n]")

def getPrediction (videoPath:str, detector:Detector) -> pd.DataFrame:
    return detector.detect_video(videoPath) #skip_frames = None

def cleanPrediction (predictions: pd.DataFrame) -> pd.DataFrame:
    #removal of unused columns
    newPredictions = predictions.filter(regex='^AU')
    return pd.concat([newPredictions, predictions["input"]], axis=1)

def getPredictionsFromVideosPaths (videoPath:list, detector:Detector, lastOne:bool) -> pd.DataFrame:
    prediciton = getPrediction (videoPath, detector)#qui ho già la predizione per tutti i frame all'interno del video
    prediciton = cleanPrediction (prediciton)
    
    if not lastOne:
        with open ((join(dirname(abspath(__file__)), "predictions.json")), "a") as f:
            f.write(prediciton.to_json(indent=4) + ",\n")
    else:
        with open ((join(dirname(abspath(__file__)), "predictions.json")), "a") as f:
            f.write(prediciton.to_json(indent=4))

def makeAndSavePredictionsOnFile (videosPathMain: list, detector:Detector) -> list [dict]:
    openListOnFile () # i save the predictions on file but the list of the objects generated is not json serializable *
    for path in tqdm(videosPathMain):
        try:
            getPredictionsFromVideosPaths(path, detector, path == videosPathMain[-1])
        except Exception as e:
            print (e)
    closeListOnFile() # * so i open and close the list on the file and save each item in append on the file 


def readPredictionsListFromFile () -> list [dict]:
    with open ((join(dirname(abspath(__file__)), "predictions.json")), "r") as f:
        data = json.load(f)

    return data