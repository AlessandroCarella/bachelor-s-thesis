import pandas as pd
from sklearn.utils import resample

from getInfoDataset import visualizeDataFrameChart

def undersampleDataset(df, columnName, valueToDownSample, numberOfSamplesAfter):
    if len(df[df[columnName] == valueToDownSample]) > numberOfSamplesAfter:
        engagedIndices = df[df[columnName] == valueToDownSample].index
        
        tempDf = df.loc[engagedIndices]
        tempDfUndersampled = tempDf.sample(n=numberOfSamplesAfter, random_state=69)
        
        print ()

        return pd.concat([df.drop(engagedIndices), tempDfUndersampled])
    return df

def oversampleDataset(df, columnName, valueToOversample, numberOfSamplesAfter):
    if len(df[df[columnName] == valueToOversample]) < numberOfSamplesAfter:
        engagedIndices = df[df[columnName] == valueToOversample].index
        
        tempDf = df.loc[engagedIndices]
        tempDfOversampled = resample(tempDf, replace=True, n_samples=numberOfSamplesAfter, random_state=69)
        
        return pd.concat([df.drop(engagedIndices), tempDfOversampled])
    return df

def resampleDataset ():
    df = pd.read_csv(r'C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\final analysis\DAiSEE and student engagement dataset clean.csv')
    visualizeDataFrameChart(df)

    numberOfValuesForEachLabel = 2000#facendo vari test questo sembra il numero di sample che mantiene più tranquillamente dei risultati e che li fa risultare più corenti nel tempo

    labelsList = df["label"].unique()
    for label in labelsList:
        df = undersampleDataset (df, "label", label, numberOfValuesForEachLabel)
    for label in labelsList:
        df = oversampleDataset (df, "label", label, numberOfValuesForEachLabel)

    visualizeDataFrameChart(df)

    df.to_csv(r'C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\final analysis\DAiSEE and student engagement dataset clean sampled.csv', index=False)

resampleDataset()