import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.naive_bayes import MultinomialNB

from randomForestClassifier import getXtrainYTrain

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getNaiveBayesClassifier():
    filePathNaiveBayesClassifier = join(dirname(abspath(__file__)), "naiveBayesClassifier.pickle")

    if isfile(filePathNaiveBayesClassifier):
        with open(filePathNaiveBayesClassifier, "rb") as f:
            naiveBayesClassifier = pickle.load(f)
    else:
        nNeib = 7
        print("Creazione Naive Bayes classifier")
        naiveBayesClassifier = MultinomialNB()
        Xtrain, yTrain, Xtest, yTest = getXtrainYTrain()
        naiveBayesClassifier.fit(Xtrain, yTrain)

        with open(filePathNaiveBayesClassifier, "wb") as f:
            pickle.dump(naiveBayesClassifier, f)
        
        #getAccuracyKnnClassifier(yTest, naiveBayesClassifier.predict(Xtest))
        #visualizeHeatMapCorrelationMatrix(Xtrain)

    return naiveBayesClassifier
