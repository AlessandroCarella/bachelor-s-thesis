import json
import os
from os.path import join, isdir, isfile, abspath, dirname, splitext
import copy

def copyVideoFirstAnalysisWithOnlyAUsAndOtherFewRelevantInfos():
    with open (join(abspath("src/analysis"), "video first analysis.json"), "r") as f:
        data = json.load(f)

    wantedKeys = ["AU01","AU02","AU04","AU05","AU06","AU07","AU09","AU10","AU11","AU12","AU14","AU15","AU17","AU20","AU23","AU24","AU25","AU26","AU28","AU43","input","frame"]

    outputData = []
    for dictionary in data:
        wanted_dict = {}
        for key, value in dictionary.items():
            if key in wantedKeys:
                wanted_dict[key] = value
        outputData.append(wanted_dict)

    with open(join(abspath("src/analysis"), "video first analysis only AUs.json"), "w") as output_file:
        json.dump(outputData, output_file, indent=4)


def getEmptyDictsWithFramesAsKeys ():
    return {
        "0.0": {},
        "60.0": {},
        "120.0": {},
        "180.0": {},
        "240.0": {},
    }

def relaborateNewDicts (newDicts):
    output = []
    for key, value in newDicts.items():
        if "input" in newDicts[key]:
            inputFileValue = splitext(newDicts[key]["input"])[0] + " frame " + str(int(float(newDicts[key]["frame"]))) + splitext(newDicts[key]["input"])[1]
            
            newDictsCopy = copy.deepcopy(newDicts)

            del newDictsCopy[key]["frame"]
            newDictsCopy[key]["input"] = inputFileValue

            output.append (newDictsCopy [key])
    return output

def saveToFile (data):
    with open (join(abspath("src/analysis"), "video analysis only AUs in images format analysis.json"), "w") as f:
        json.dump (data, f, indent=4)

def fromVideoJsonToImageLikeJson ():
    with open(join(abspath("src/analysis"), "video first analysis only AUs.json"), "r") as f:
        data = json.load(f)

    newData = []
    for elem in data:
        newDicts = getEmptyDictsWithFramesAsKeys ()
        for key, value in elem.items():
            for subKey, subValue in value.items():
                if subKey in newDicts:
                    newDicts[subKey][key] = subValue
        newData.extend(relaborateNewDicts(newDicts))
        saveToFile (newData)
                

fromVideoJsonToImageLikeJson ()