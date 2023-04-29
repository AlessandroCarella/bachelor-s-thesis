import os
from os.path import join, isdir, isfile, abspath, dirname, sep, basename
import json
import pandas as pd
from tqdm import tqdm
import csv

from naturalLanguageDescriptionFromAU import getAnalyses, getNewOutPaths

def changeExtension(path, new_extension):
    root, old_extension = os.path.splitext(path)
    return root + "." + new_extension

def getRefactorPaths (paths, newFolder, extension):
    output = []
    for path in paths:
        folders = dirname(path).split(sep)
        fileName = basename(path)
        output.append(join (abspath ("src"), "analysis", newFolder, folders[-3] + " " + folders[-2] + " " + folders[-1] + " " + changeExtension(fileName, extension)))
    return output

def saveDfToFileJson (df: pd.DataFrame, path):
    with open (path, "w") as f:
        json.dump(json.loads(df.to_json (orient="records")), f, indent=4)

def saveDfToFileCsv (df: pd.DataFrame, path):
    df.to_csv (path, index = False)

def cleanDf (df: pd.DataFrame):
    return df.drop (
            ["FaceRectX", "FaceRectY", "FaceRectWidth", "FaceRectHeight", "FaceScore", "x_0", "x_1", "x_2", "x_3", "x_4", "x_5", "x_6", "x_7", "x_8", "x_9", "x_10", "x_11", "x_12", "x_13", "x_14", "x_15", "x_16", "x_17", "x_18", "x_19", "x_20", "x_21", "x_22", "x_23", "x_24", "x_25", "x_26", "x_27", "x_28", "x_29", "x_30", "x_31", "x_32", "x_33", "x_34", "x_35", "x_36", "x_37", "x_38", "x_39", "x_40", "x_41", "x_42", "x_43", "x_44", "x_45", "x_46", "x_47", "x_48", "x_49", "x_50", "x_51", "x_52", "x_53", "x_54", "x_55", "x_56", "x_57", "x_58", "x_59", "x_60", "x_61", "x_62", "x_63", "x_64", "x_65", "x_66", "x_67", "y_0", "y_1", "y_2", "y_3", "y_4", "y_5", "y_6", "y_7", "y_8", "y_9", "y_10", "y_11", "y_12", "y_13", "y_14", "y_15", "y_16", "y_17", "y_18", "y_19", "y_20", "y_21", "y_22", "y_23", "y_24", "y_25", "y_26", "y_27", "y_28", "y_29", "y_30", "y_31", "y_32", "y_33", "y_34", "y_35", "y_36", "y_37", "y_38", "y_39", "y_40", "y_41", "y_42", "y_43", "y_44", "y_45", "y_46", "y_47", "y_48", "y_49", "y_50", "y_51", "y_52", "y_53", "y_54", "y_55", "y_56", "y_57", "y_58", "y_59", "y_60", "y_61", "y_62", "y_63", "y_64", "y_65", "y_66", "y_67", "Pitch", "Roll", "Yaw", "anger", "disgust", "fear", "happiness", "sadness", "surprise", "neutral", "frame"], 
            axis=1
        )


analyses, outPaths = getAnalyses ()    
outPathsWithNaturalLanguage = getNewOutPaths (outPaths)


outPathsNewPathsJsonNotClean = getRefactorPaths (outPaths, join("json", "all parameters", "plain"), "json")
outPathsNewPathsJsonClean = getRefactorPaths (outPaths, join("json", "only AUs", "plain"), "json")

outPathsNewPathsCsvNotClean = getRefactorPaths (outPaths, join("csv", "all parameters", "plain"), "csv")
outPathsNewPathsCsvClean = getRefactorPaths (outPaths, join("csv", "only AUs", "plain"), "csv")


outPathsWithNaturalLanguageNewPathsJsonNotClean = getRefactorPaths (outPathsWithNaturalLanguage, join("json", "all parameters", "with natural language description"), "json")
outPathsWithNaturalLanguageNewPathsJsonClean = getRefactorPaths (outPathsWithNaturalLanguage, join("json", "only AUs", "with natural language description"), "json")

outPathsWithNaturalLanguageNewPathsCsvNotClean = getRefactorPaths (outPathsWithNaturalLanguage, join("csv", "all parameters", "with natural language description"), "csv")
outPathsWithNaturalLanguageNewPathsCsvClean = getRefactorPaths (outPathsWithNaturalLanguage, join("csv", "only AUs", "with natural language description"), "csv")

for i in tqdm(range(len(outPaths))):
    df = pd.read_json (outPaths[i])
    saveDfToFileJson (df, outPathsNewPathsJsonNotClean [i])
    saveDfToFileCsv (df, outPathsNewPathsCsvNotClean [i])

    df = cleanDf (df)
    saveDfToFileJson (df, outPathsNewPathsJsonClean [i])
    saveDfToFileCsv (df, outPathsNewPathsCsvClean [i])
    

for i in tqdm(range(len(outPathsWithNaturalLanguage))):
    df = pd.read_json (outPathsWithNaturalLanguage[i])
    saveDfToFileJson (df, outPathsWithNaturalLanguageNewPathsJsonNotClean [i])
    saveDfToFileCsv (df, outPathsWithNaturalLanguageNewPathsCsvNotClean [i])

    df = cleanDf (df)
    saveDfToFileJson (df, outPathsWithNaturalLanguageNewPathsJsonClean [i])
    saveDfToFileCsv (df, outPathsWithNaturalLanguageNewPathsCsvClean [i])