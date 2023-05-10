import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from randomForestClassifier import getXtrainYTrain

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getKnnClassifier():
    filePathKnnClassifier = join(dirname(abspath(__file__)), "KnnClassifier.pickle")

    if isfile(filePathKnnClassifier):
        with open(filePathKnnClassifier, "rb") as f:
            KnnClassifier = pickle.load(f)
    else:
        print("Creazione Knn classifier")
        KnnClassifier = KNeighborsClassifier(n_neighbors=5)
        Xtrain, yTrain, Xtest, yTest = getXtrainYTrain()
        KnnClassifier.fit(Xtrain, yTrain)
        
        #visualizeFeaturesImportances(randomForestClassifier, datasetWithoutLabelCol)
        #randomForestClassifierVisualize(randomForestClassifier)

        with open(filePathKnnClassifier, "wb") as f:
            pickle.dump(KnnClassifier, f)
        
        # Predict the labels of the test data
        yPred = KnnClassifier.predict(Xtest)

        # Evaluate the accuracy of the classifier
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(yTest, yPred)
        print("Accuracy: ", accuracy)

    return KnnClassifier
