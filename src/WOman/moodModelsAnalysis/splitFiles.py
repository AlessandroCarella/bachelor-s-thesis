from os.path import join, abspath, dirname, basename, splitext, exists
from os import listdir, makedirs

def makeAndGetDirDictToFile (filePath):
    folderName = splitext(basename(filePath))[0].replace('.', "")
    folderPath = join(filePath, "..", "..", "splittedMoodModels", folderName)
    if not exists(folderPath):
        makedirs(folderPath)
    return folderPath

def saveDictToFile (actionsDict, filePath):
    folderPath = makeAndGetDirDictToFile(filePath)
    i = 0
    for key, value in actionsDict.items():
        #remove the last char ("(") in the key string
        with open (join (folderPath, str (i) + " " + key[:-1] + ".txt"), "w") as f:
            for elem in value:
                f.write(elem + "\n")
        i += 1
    
def splitFile (filePath, actionsDict):
    with open(filePath, 'r') as f:
        filelines = f.readlines()
    
    for line in filelines:
        for action in actionsDict.keys():
            if line.startswith(action):
                actionsDict[action].append(line.replace(action, "").replace (").\n", ""))
    
    saveDictToFile (actionsDict, filePath)
    
def getActions ():
    actions = []
    with open (join(dirname(__file__), "actions.txt"), "r") as f:
        for line in f.readlines():
            actions.append (line.replace ("\n", "") + "(")
    return actions

def getActionsDict ():
    actionsDict = {}
    actions = getActions()
    for action in actions:
        actionsDict[action] = []
    return actionsDict

def main ():
    folderPath = join(dirname(__file__), "moodModels")
    for file in listdir(folderPath):
        filePath = join(folderPath, file)
        splitFile (filePath, getActionsDict ())
