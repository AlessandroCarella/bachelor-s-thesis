import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.svm import SVC

from randomForestClassifier import getXtrainYTrain
from KnnClassifier import getModelAccuracy

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getSVMClassifier():
    filePathSVMClassifier = join(dirname(abspath(__file__)), "SVMClassifier.pickle")

    if isfile(filePathSVMClassifier):
        with open(filePathSVMClassifier, "rb") as f:
            SVMClassifier = pickle.load(f)
    else:
        nNeib = 7
        print("Creazione Support Vector Machines classifier")
        # Create a SVM classifier object
        SVMClassifier = SVC(kernel='linear', random_state=69, probability=True)

        Xtrain, yTrain, Xtest, yTest = getXtrainYTrain()
        SVMClassifier.fit(Xtrain, yTrain)

        with open(filePathSVMClassifier, "wb") as f:
            pickle.dump(SVMClassifier, f)
        
        getModelAccuracy(yTest, SVMClassifier.predict(Xtest))
        #visualizeHeatMapCorrelationMatrix(Xtrain)

    return SVMClassifier