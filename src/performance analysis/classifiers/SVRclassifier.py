import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.svm import SVC
from sklearn.svm import SVR
import numpy as np

#from classifiers.randomForestClassifier import getXtrainYTrainXtestYTest#, getModelScores
#from randomForestClassifier import getXtrainYTrainXtestYTest#, getModelScores

def fromNumLabelToLabel (numLabel):
    if numLabel == 0:
        return "confused"
    elif numLabel == 1:
        return "engaged"
    elif numLabel == 2:
        return "frustrated"
    elif numLabel == 3:
        return "bored"
    elif numLabel == 4:
        return "drowsy"
    elif numLabel == 5:
        return "looking away"

from sklearn.model_selection import train_test_split
def getXtrainYTrainXtestYTest():
    # Load the dataset
    df = pd.read_csv(join(dirname(abspath(__file__)), "../../final analysis/DAiSEE and student engagement dataset clean sampled.csv"))

    # Split the dataset into features and target variable
    y = df['numLabel']
    X = df.drop(["input","naturalLanguageDescription","label","numLabel"], axis=1)

    # Split the dataset into training and testing sets
    Xtrain, Xtest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=69)

    return Xtrain, yTrain, Xtest, yTest


def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getAccuracyNaiveBayesClassifier(SVMClassifier, Xtest, yTest):
    print("Accuracy on Xtest:", SVMClassifier.score(Xtest, yTest))

def getSVRClassifier():
    filePathSVMClassifier = join(dirname(abspath(__file__)), "serializedObjects/SVMClassifier.pickle")

    if isfile(filePathSVMClassifier):
        with open(filePathSVMClassifier, "rb") as f:
            SVMClassifier = pickle.load(f)
    else:
        print("Creazione Support Vector Machines classifier")
        # Create a SVM classifier object
        """SVMClassifier = SVC(kernel='linear', random_state=69, probability=True)"""
        SVMClassifier = SVR(kernel='linear')

        Xtrain, yTrain, Xtest, yTest = getXtrainYTrainXtestYTest()
        from sklearn.preprocessing import LabelEncoder
        yTrain = LabelEncoder().fit_transform(yTrain)
        SVMClassifier.fit(Xtrain, yTrain)

        #with open(filePathSVMClassifier, "wb") as f:
        #   pickle.dump(SVMClassifier, f)
        
        #for score in getModelScores(yTest, SVMClassifier.predict(Xtest)):
        #    print (score)
        #    print()

        print (SVMClassifier.score(Xtest, yTest))

        #getAccuracyNaiveBayesClassifier(SVMClassifier, Xtest, yTest)
        #visualizeHeatMapCorrelationMatrix(Xtrain)

    return SVMClassifier

getSVMClassifier ()