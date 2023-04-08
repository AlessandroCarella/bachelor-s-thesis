import os
from os.path import join, isdir, isfile, abspath, dirname
import json
from tqdm import tqdm

def getJsonListFromFile (path):
    fileLines = []
    with open (path, "r") as f:
        fileLines = f.readlines()

    fileLines = fileLines[1:-1]
    for i in range(len(fileLines)):
        fileLines[i] = fileLines[i].strip()
        fileLines[i] = fileLines[i][1:-2] + ","

        fileLines[i] = fileLines[i].replace('\\"', '"')
        fileLines[i] = fileLines[i].replace('\\\\\\\\', '/')

    fileLines [-1] = fileLines[-1][:-1]
    fileLines [-1] = fileLines[-1] +  "}"

    fileLines.insert (0, "[")
    fileLines.append ("]")

    fileLines = "".join(fileLines)

    fileList = json.loads(fileLines)

    return fileList

def cleanFromZero (data):
    output = []
    for element in data:
        elem = {}
        for key, value in element.items():
            elem[key] = value["0"]
        output.append(elem) 
    return output

def cleanAndIndentAnalysis():
    allFoldersWithImagesPathsAndRelativeImagesPaths = {}
    with open (join(abspath ("src"), "allFoldersWithImagesPathsAndRelativeImagesPaths.json"), "r") as f:
        allFoldersWithImagesPathsAndRelativeImagesPaths = json.load(f)

    for key, value in tqdm(allFoldersWithImagesPathsAndRelativeImagesPaths.items()):
        path = join(key, "analysis.json")
        elementsList = cleanFromZero(getJsonListFromFile (path))
        with open(path, 'w') as f:
            json.dump (elementsList, f, indent=4)

cleanAndIndentAnalysis ()