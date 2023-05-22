from os.path import normpath, splitext, basename
import pandas as pd
import re

from reorderEntries import reorderEntries

def findLabel (videoPath:str, DAiSEE: pd.DataFrame) -> str:
    #return "engaged"
    
    videoFileName = splitext(normpath(videoPath).split("\\")[-1])[0]
    #seleziono la riga del dataset nella quale c'è il file di inpu e estraggo la label da li
    #siccome ci sono diverse righe per il file di input in quanto il dataset ha più valori di
    #AUs per i vari frame estratti dal singolo video (uno ogni 30 frame) ho bisogno di inseriere
    #.tolist()[0] per prendere la label del primo risultato ottenuto (tutte le righe estratte hanno)
    #lo stesso valore di label
    return DAiSEE.loc[DAiSEE['input'].str.contains(videoFileName), 'label'].tolist()[0]

def getNumberOfFrameUse(frame:str, outputStrings:list[str], maxNumberOfCharsForUseOfFrame:int) -> int:
    if len (outputStrings) == 0:
        return 0
    
    frame = int (frame)

    numberOfFrameUse = 0
    for outputStr in outputStrings:
        #es:
        #Entry(000020,begin_of_activity,engaged,v32,au1,1).
        #     0              1             2     3   4  5
        frameAndNumberOfUse = outputStr.split(",")[0]
        frameTemp = int(re.sub("[^0-9]", "", frameAndNumberOfUse[:-maxNumberOfCharsForUseOfFrame]))
        if frameTemp == frame:
            numberOfFrameUse += 1
    
    return numberOfFrameUse

def getNumberOfActivityForAU (actionUnit:str, outputStrings:list[str]) -> int:
    numberOfBeginOfActivityForAU = 0
    for outputStr in outputStrings:
        outputStrSplit = outputStr.split(",")
        #es:
        #Entry(000020,begin_of_activity,engaged,v32,au1,1).
        #     0              1             2     3   4  5
        if "end_of_activity" in outputStrSplit[1]:
            actionUnitTemp = outputStrSplit[4]
            if actionUnitTemp == actionUnit:
                numberOfBeginOfActivityForAU += 1
            
    return numberOfBeginOfActivityForAU

def getEntryText (frame:str, activityOrProcessBeginOrEndStr:str, label:str, inputFile:str, actionUnit:str, maxNumberOfCharsForFrames:int, maxNumberOfCharsForUseOfFrame:int, outputStrings:list[str]) -> str:
    AUlow = actionUnit.lower()

    entryString = "entry("
    entryString += '{0:0{1}d}'.format(int(frame), maxNumberOfCharsForFrames)
    entryString += '{0:0{1}d}'.format(getNumberOfFrameUse(frame, outputStrings, maxNumberOfCharsForUseOfFrame), maxNumberOfCharsForUseOfFrame)
    entryString += ","
    entryString += activityOrProcessBeginOrEndStr.lower()
    entryString += ","
    entryString += label.lower()
    entryString += ","
    entryString += "video" + inputFile
    entryString += ","
    entryString += AUlow
    entryString += ","
    entryString += str(getNumberOfActivityForAU (AUlow, outputStrings))
    entryString += ")."
    return entryString

def closeAllOpenedAUs (lastFrame:str, activityOrProcessBeginOrEndStr:str, label:str, inputFile:str, activeActionUnits:list[str], maxNumberOfCharsForFrames:int, maxNumberOfCharsForUseOfFrame:int, outputStrings:list[str]) -> list[str]:
    closingLinesForActiveActionUnits = []
    
    for actionUnit in activeActionUnits:
        closingLinesForActiveActionUnits.append(
            getEntryText (
                lastFrame,
                activityOrProcessBeginOrEndStr,
                label,
                inputFile,
                actionUnit,
                maxNumberOfCharsForFrames,
                maxNumberOfCharsForUseOfFrame,
                outputStrings
            )
        )

    return closingLinesForActiveActionUnits

def getSingleVideoExtraction (singleVideoData:dict, DAiSEE: pd.DataFrame, actionUnitsThreshold:float) -> dict:
    """
    (T, E, W, P, A, O), where
    T is the time/date the event occurred, 
    E is the type of the event (begin of process, end of process, begin of activity, end of activity), 
    W is the name of the workflow the event refers to, 
    P is a unique identifier for each process execution, 
    A is the name of the activity, 
    O is the progressive number of occurrences of A in P

    Entry(000020,begin_of_activity,engaged,v32,au1,1).
    Entry(
    T   numeroFrame|numeroUtilizzoFrame, 
    E   begin_of_activity|end_of_activity|begin_of_process|end_of_process,
    W   label,
    P   inputFilePath,
    A   Action Unit che si è accesa/spenta in qual momento
    O   numero di begin_of_activity per quella AU
    )
    numeroUtilizzoFrame è perchè durante lo stesso frame potrebbe "accendersi" un'AU e spegnersene un'altra o accendersene un'altra ancora
    """
    activeActionUnits = []
    numberOfFrames = len(singleVideoData["input"])
    maxNumberOfCharsForFrames = len(str(numberOfFrames))
    maxNumberOfCharsForUseOfFrame = len(str(len(singleVideoData)))


    inputFile = splitext(basename(singleVideoData["input"]["0"]))[0]
    del singleVideoData["input"]
    label = findLabel (inputFile, DAiSEE)
    outputStrings = [ #inizializzazione
        getEntryText(
            0,
            "begin_of_process",
            label,
            inputFile,
            "start",
            maxNumberOfCharsForFrames,
            maxNumberOfCharsForUseOfFrame,
            []
        )
    ]
    
    for actionUnit, framesDict in singleVideoData.items (): #itero sulle action units
        for frame, value in framesDict.items (): #itero sui frame relativi all'action unit che sto analizzando ora
            if float(value) >= actionUnitsThreshold and actionUnit not in activeActionUnits:
                activeActionUnits.append(actionUnit)
                outputStrings.append(
                    getEntryText(
                        frame,
                        "begin_of_activity",
                        label,
                        inputFile,
                        actionUnit,
                        maxNumberOfCharsForFrames,
                        maxNumberOfCharsForUseOfFrame,
                        outputStrings
                    )
                )
            else:
                if actionUnit in activeActionUnits:
                    activeActionUnits.remove(actionUnit)
                    outputStrings.append(
                        getEntryText(
                            frame,
                            "end_of_activity",
                            label,
                            inputFile,
                            actionUnit,
                            maxNumberOfCharsForFrames,
                            maxNumberOfCharsForUseOfFrame,
                            outputStrings
                        )
                    )

    outputStrings.extend(
        closeAllOpenedAUs (
            numberOfFrames - 1, 
            "end_of_activity",
            label,
            inputFile,
            activeActionUnits, 
            maxNumberOfCharsForFrames,
            maxNumberOfCharsForUseOfFrame,
            outputStrings
            )
        )
    
    outputStrings.append (
            getEntryText(
                numberOfFrames,
                "end_of_process",
                label,
                inputFile,
                "stop",
                maxNumberOfCharsForFrames,
                maxNumberOfCharsForUseOfFrame,
                outputStrings
            )
        )
        
    return {splitext(basename(inputFile))[0]:reorderEntries(outputStrings, maxNumberOfCharsForFrames, maxNumberOfCharsForUseOfFrame)}