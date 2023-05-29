import json 
from os.path import basename, dirname, join, abspath
import pandas as pd

with open (join(dirname(abspath(__file__)), "predictions.json"), "r") as f:
    data = json.load(f)

inputFiles = []
for elem in data:
    inputFiles.append(elem["input"]["0"])

inputFilesNames = []
for file in inputFiles:
    inputFilesNames.append(basename(file))

allVideos = pd.read_csv(join(dirname(abspath(__file__)), "AllLabelsDAiSEE.csv")) ["ClipID"].tolist ()

missingVideos = []
for inputFileName in inputFilesNames:
    if (inputFileName not in allVideos):
        missingVideos.append(inputFileName)

print ("dimensione lista video mancanti")
print (len(missingVideos))
print ("video mancanti:")
for video in missingVideos:
    print (video)