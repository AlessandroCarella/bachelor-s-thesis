import os
from os.path import join, isdir, isfile, abspath, dirname, sep
import json

def getAUs ():
    with open(join(abspath ("src"), "AUs.json")) as f:
        AUs = json.loads(f.read())
    return AUs

def getAnalyses ():
    outPaths = []

    with open (join(abspath ("src"), "allFoldersWithImagesPathsAndRelativeImagesPaths.json")) as f:
        allFoldersWithImagesPathsAndRelativeImagesPaths = json.loads(f.read())

    analysesPaths = []
    for key, value in allFoldersWithImagesPathsAndRelativeImagesPaths.items():
        analysesPaths.append(join(key, "analysis.json"))
    
    analyses = {}
    for path in analysesPaths:
        outPaths.append (path)
        with open (path) as f:
            analysis = json.loads(f.read())
        folders = dirname(path).split(sep)
        analyses [folders[-3] + " " + folders[-2] + " " + folders[-1]] = analysis

    return analyses, outPaths

def getNewOutPaths (outPaths):
    output = []
    for path in outPaths:
        output.append(join (dirname (path), "analysisWithNaturalLanuageDescription.json"))
    return output

def getPossibleAUsNames ():
    possibleAUsNames = []
    base = "AU"

    for i in range(1, 67):
        possibleAUsNames.append(base + str(i))

    return possibleAUsNames

def makeAUDescription (AUName, AUs, value):
    for au in AUs:
        if au.get("AU") == AUName:
            outAU = au
            break
    return outAU.get ("FACS Name") + ", using the muscles: " + outAU.get ("Muscles") + ", with a value of " + str (value) + "\n"

def getNaturalLanguageDescription (sample:dict, possibleAUsNames:list, AUs:list):
    naturalLanguageDescription = ""
    for AUName in possibleAUsNames:
        if AUName in sample:
            naturalLanguageDescription += makeAUDescription (AUName, AUs, value = sample [AUName])
    return naturalLanguageDescription

def saveToJsonFile (value, outPath):
    with open (outPath, "w") as f:
        json.dump(value, f, indent=4)

def naturalLanguageDescriptionFromAU ():
    AUs = getAUs ()
    analyses, outPaths = getAnalyses ()
    outPaths = getNewOutPaths (outPaths)
    possibleAUsNames = getPossibleAUsNames ()

    iteratorOutPaths = 0
    for key, value in analyses.items():
        for i in range(len(value)):
            sample = value [i]
            value [i]["naturalLanguageDescription"] = getNaturalLanguageDescription (sample, possibleAUsNames, AUs)
        saveToJsonFile (value, outPaths [iteratorOutPaths])
        iteratorOutPaths += 1