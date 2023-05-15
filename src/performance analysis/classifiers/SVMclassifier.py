import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.svm import SVC

from classifiers.randomForestClassifier import getXtrainYTrainXtestYTest#, getModelScores
#from randomForestClassifier import getXtrainYTrainXtestYTest#, getModelScores

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getAccuracyNaiveBayesClassifier(SVMClassifier, Xtest, yTest):
    print("Accuracy on Xtest:", SVMClassifier.score(Xtest, yTest))

def getSVMClassifier():
    filePathSVMClassifier = join(dirname(abspath(__file__)), "serializedObjects/SVMClassifier.pickle")

    if isfile(filePathSVMClassifier):
        with open(filePathSVMClassifier, "rb") as f:
            SVMClassifier = pickle.load(f)
    else:
        nNeib = 7
        print("Creazione Support Vector Machines classifier")
        # Create a SVM classifier object
        SVMClassifier = SVC(kernel='linear', random_state=69, probability=True)

        Xtrain, yTrain, Xtest, yTest = getXtrainYTrainXtestYTest()
        SVMClassifier.fit(Xtrain, yTrain)

        with open(filePathSVMClassifier, "wb") as f:
            pickle.dump(SVMClassifier, f)
        
        #for score in getModelScores(yTest, SVMClassifier.predict(Xtest)):
        #    print (score)
        #    print()

        #getAccuracyNaiveBayesClassifier(SVMClassifier, Xtest, yTest)
        #visualizeHeatMapCorrelationMatrix(Xtrain)

    return SVMClassifier