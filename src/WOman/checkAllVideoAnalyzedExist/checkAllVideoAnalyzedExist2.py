import json 
from os.path import basename, dirname, join, abspath
import pandas as pd

def getHighestValuePos (myList):
    return myList.index(max(myList))

def getAllLabels (allVideos):
    labelsAndFiles = []
    for elem in allVideos:
        values = [elem ["Boredom"], elem ["Engagement"], elem ["Confusion"], elem ["Frustration "]]
        highestValuePos = getHighestValuePos(values)
        if highestValuePos == 0:
            labelsAndFiles.append({"clipID": elem["ClipID"], "label": "bored", "numLabel": 3})
        elif highestValuePos == 1:
            labelsAndFiles.append({"clipID": elem["ClipID"], "label": "engaged", "numLabel": 1})
        elif highestValuePos == 2:
            labelsAndFiles.append({"clipID": elem["ClipID"], "label": "confused", "numLabel": 0})
        elif highestValuePos == 3:
            labelsAndFiles.append({"clipID": elem["ClipID"], "label": "frustrated", "numLabel": 2})
    return labelsAndFiles


def main ():
    with open (join(dirname(abspath(__file__)), "predictions.json"), "r") as f:
        data = json.load(f)

    allVideos = pd.read_csv(join(dirname(abspath(__file__)), "AllLabelsDAiSEE.csv")).to_dict('records')
    labelsAndFiles = getAllLabels (allVideos)

    misMatch = []
    for elem in data:
        for labelAndFile in labelsAndFiles:
            if basename(elem["input"]["0"]) == labelAndFile ["clipID"]:
                if labelAndFile ["label"] != elem["label"]:
                    misMatch.append({"labelAndFile":labelAndFile, "jsonLabel":elem["label"], "csvLabel":labelAndFile ["label"]})
    
    print (len(misMatch))
    for elem in misMatch:
        print(elem)

main()