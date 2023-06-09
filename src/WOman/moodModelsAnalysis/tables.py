"""
numero di task,
numero di transition, 
numero di eventi,
numero di attivita
"""
from os.path import join, abspath, dirname, basename, splitext, exists
from os import listdir

def getNumberFromFile (filePath):
    with open (filePath) as f:
        n = f.readline ()
    return n


folderPath = join(dirname(__file__), "splittedMoodModels")

for folder in listdir(folderPath):
    if folder != "results":
        for file in listdir(join(folderPath, folder)):
            filePath = join(folderPath, folder, file)
            if file == "26 counter.txt":
                taskNumber = getNumberFromFile (filePath)
            elif file == "20 transition_counter.txt":
                transitionNumber = getNumberFromFile (filePath)

        resultsFilePath = join(folderPath, "results", folder + ".txt")# e.g: folderPath/results/bored.txt
        with open (resultsFilePath, "w") as f:
            f.writelines ([
                    "numero di task: " + str(taskNumber),
                    "numero di transizioni: " + str (transitionNumber),
                ])
