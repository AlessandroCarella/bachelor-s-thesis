import os
from os.path import join, isdir, isfile, abspath, dirname
import json

def getPicsNames (folderPath):
    picsNames = []
    for file in os.listdir (folderPath):
        if file.endswith (".jpg"):
            picsNames.append (file) 
    return picsNames

def getPicFoldersPaths (originalPath):
    picFoldersPaths = []
    for filename in os.listdir (originalPath):
        fileOrFolderPath = join (originalPath, filename)
        if isdir(fileOrFolderPath):
            picFoldersPaths.extend(getPicFoldersPaths(fileOrFolderPath))
        elif isfile(fileOrFolderPath):
            picFoldersPaths.append (dirname(fileOrFolderPath))
            break
    return picFoldersPaths
            
def getAllFoldersWithImagesPathsAndRelativeImagesPaths ():
    picsDict = {}
    datasetFolder = abspath ("datasets")

    for folderPath in getPicFoldersPaths (datasetFolder):
        picsDict.update ({
            folderPath
            :
            getPicsNames (folderPath)
            }) 

    with open (join(abspath ("src"),"allFoldersWithImagesPathsAndRelativeImagesPaths.json"), "w") as f:
        json.dump (picsDict, f, indent=4)

getAllFoldersWithImagesPathsAndRelativeImagesPaths ()
