import json
import os
from os.path import join, isdir, isfile, abspath, dirname, normpath, getsize, splitext, exists
import sys

def getNewFileName (fileName, i):
    fileName, extension = splitext (fileName)
    return fileName + " " + str(i) + extension

def saveToFile (filename, data):
    with open (filename, "w") as f:
        json.dump (data, f, indent=4)
    return getsize (filename) / (1024*1024)

def splitJsonFile (fileName):
    fileSize = getsize(fileName) / (1024*1024)
    with open (fileName, "r") as f:
        data = json.load (f)
    
    i = 0
    maxFileSize = 80 #100 in verità per git ma preferisco mantenerlo più basso
    totalNumberOfFIles = (fileSize/maxFileSize) + 1
    while i < totalNumberOfFIles:
        writeData = []
        newFileName = getNewFileName (fileName, i)
        j = 0
        skipValue = 400 #change this value based on the single elements of the json, i try to get 1 mb for each iteration, so the time of execution is (totalNumberOfFIles * 100)seconds
        for j in range (len(data)):
            writeData.append (data[j:j+skipValue])
            j += skipValue 
            print (sys.getsizeof(json.dumps(writeData, indent=4)) / (1024*1024))
            if (sys.getsizeof(json.dumps(writeData, indent=4)) / (1024*1024)) > maxFileSize:
                i += 1
                saveToFile (newFileName, writeData)
                break

    print (fileSize)

splitJsonFile ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/video first analysis.json")


def getDataFromSplittedJsonFile (fileName): 
    # input fileName = uno dei file numerati senza il numero e con l'estensione json:
    # es:
    # video first analysis 0.json (che avrà poi la versione 1,2,3,...)
    # -->
    # video first analysis.json
    i = 0
    outputData = []
    while exists(getNewFileName (fileName, i)):
        with open (getNewFileName (fileName, i), "r") as f:
            outputData.extend (json.load (f))
    return outputData