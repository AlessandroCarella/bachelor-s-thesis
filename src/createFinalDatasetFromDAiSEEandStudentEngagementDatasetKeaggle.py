import os
from os.path import join, isdir, isfile, abspath, dirname, sep, basename, splitext
import json
import pandas as pd
from tqdm import tqdm
import csv

"""
lables in student engagement dataset:
enaged:
    confused 0
    engaged 1
    frustated 2
not engaged:
    bored 3
    drowsy 4
    looking away 5
"""

def getHighestValuePos (myList):
    return myList.index(max(myList))

def getDAiSEEjsonWithFileLabelAndNumericLabel ():
    threeLabelsAndFile = pd.read_csv('C:/Users/Alessandro/Desktop/bachelor-s-thesis/datasets/DAiSEE/Labels/AllLabels.csv').to_dict('records')
    """
    lables in student engagement dataset:
    enaged:
        confused 0
        engaged 1
        frustated 2
    not engaged:
        bored 3
        drowsy 4
        looking away 5
    """
    singleLabelAndFile = []
    for elem in threeLabelsAndFile:
        values = [elem ["Boredom"], elem ["Engagement"], elem ["Confusion"], elem ["Frustration "]]
        highestValuePos = getHighestValuePos(values)
        if highestValuePos == 0:
            singleLabelAndFile.append({"clipID": elem["ClipID"], "label": "bored", "numLabel": 3})
        elif highestValuePos == 1:
            singleLabelAndFile.append({"clipID": elem["ClipID"], "label": "engaged", "numLabel": 1})
        elif highestValuePos == 2:
            singleLabelAndFile.append({"clipID": elem["ClipID"], "label": "confused", "numLabel": 0})
        elif highestValuePos == 3:
            singleLabelAndFile.append({"clipID": elem["ClipID"], "label": "frustated", "numLabel": 2})
        # else is not handled so this filters out the irresolute cases


    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE file, label e label numerica.json", "w") as f:
        json.dump(singleLabelAndFile, f, indent=4)


def getAllFilesPathsWithAUsData ():
    return [
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/video analysis only AUs in images format analysis with natural language description.json"
    ]

def getAllFilesPathsWithLabels ():
    return [
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE file, label e label numerica.json",
    ]

def getFileNameFromInputFieldAUsData (inputField:str):
    return splitext(inputField.split ("//") [11])[0]

def getFinalDAiSEEwithAUsInputFileNaturalLanguageDescriptionAndLabelsJson ():
    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/video analysis only AUs in images format analysis with natural language description.json") as f:
        AUsData = json.load(f)

    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE file, label e label numerica.json") as f:
        fileAndLabelsData = json.load(f)

    AUsData = {getFileNameFromInputFieldAUsData(d ["input"]) : d for d in AUsData}
    fileAndLabelsData = {splitext(d['clipID'])[0]: {'label': d['label'], 'numLabel': d['numLabel']} for d in fileAndLabelsData}

    newFileAndLabelsData = {}
    for key, value in fileAndLabelsData.items():
        newFileAndLabelsData [key + " frame 0"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 30"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 60"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 90"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 120"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 150"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 180"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 210"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 240"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 270"] = fileAndLabelsData[key]
        newFileAndLabelsData [key + " frame 300"] = fileAndLabelsData[key]
    fileAndLabelsData = newFileAndLabelsData

    output = []

    for key, value in tqdm(AUsData.items()):
        if key in fileAndLabelsData:
            newElem = value
            newElem ["label"] = fileAndLabelsData[key]["label"]
            newElem ["numLabel"] = fileAndLabelsData[key]["numLabel"]
            output.append(newElem)
        
    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE Aus, input file, natural language description e labels.json", "w") as f:
        json.dump(output, f, indent=4)


def getLabelFromPath (path, alreadyFrustrated):
    label = path.split ("/")[10].split (" ")[2]
    if alreadyFrustrated:
        label = path.split ("/")[10].split (" ")[3]
    if label == "Looking":
        return "looking away"
    return label

def getNumLabelFromLabel (label):
    if label == "confused":
        return 0
    elif label == "engaged":
        return 1
    elif label == "frustrated":
        return 2
    elif label == "bored":
        return 3
    elif label == "drowsy":
        return 4
    elif label == "looking away":
        return 5

def getFinalStudentEngagementDatasetWithAUsInputFileNaturalLanguageDescriptionAndLabelsJson ():
    paths = [
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/json/only AUs/with natural language description/Student-engagement-dataset Engaged confused analysisWithNaturalLanuageDescription.json",
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/json/only AUs/with natural language description/Student-engagement-dataset Engaged engaged analysisWithNaturalLanuageDescription.json",
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/json/only AUs/with natural language description/Student-engagement-dataset Engaged frustrated analysisWithNaturalLanuageDescription.json",
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/json/only AUs/with natural language description/Student-engagement-dataset Not engaged bored analysisWithNaturalLanuageDescription.json",
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/json/only AUs/with natural language description/Student-engagement-dataset Not engaged drowsy analysisWithNaturalLanuageDescription.json",
        "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/json/only AUs/with natural language description/Student-engagement-dataset Not engaged Looking Away analysisWithNaturalLanuageDescription.json",
    ]


    alreadyFrustrated = False
    output = []
    for path in paths:
        label = getLabelFromPath (path, alreadyFrustrated)
        if label == "frustrated":
            alreadyFrustrated = True
        numLabel = getNumLabelFromLabel (label)
        with open (path) as f:
            data = json.load(f)
        
        for elem in data:
            elem ["label"] = label
            elem ["numLabel"] = numLabel
        
        output.extend (data)

    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/Student engagement dataset keaggle Aus, input file, natural language description e labels.json", "w") as f:
        json.dump(output, f, indent=4)

def mergeJsonDatasetsInCsv ():
    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/Student engagement dataset keaggle Aus, input file, natural language description e labels.json") as f:
        studentEngagementDataset = json.load (f)
    
    with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE Aus, input file, natural language description e labels.json") as f:
        DAiSEEdataset = json.load (f)
    
    pd.DataFrame(
                studentEngagementDataset + DAiSEEdataset
            ).to_csv (
                r"C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE and student engagement dataset.csv", 
                index = None
            )
    