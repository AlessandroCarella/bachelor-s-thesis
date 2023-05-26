from os.path import normpath, splitext, basename
import pandas as pd
import re

from getSingleVideoExtractionUtility import getEntryText, closeAllOpenedAUs
from reorderEntries import reorderEntries

def getSingleVideoExtraction (singleVideoData:dict, label: str, actionUnitsThreshold:float) -> dict:
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
        if not isinstance (framesDict, str):#lables are str not dict
            for frame, value in framesDict.items (): #itero sui frame relativi all'action unit che sto analizzando ora
                if value is None:#sometimes the Detector doesn't find a value for the action unit
                    value = 0 #i set it ot 0 so that the program doesn't crash and the behavior doesn't change
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