import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

from classifiers.randomForestClassifier import getXtrainYTrainXtestYTest, getModelScores
#from randomForestClassifier import getXtrainYTrainXtestYTest

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getAccuracyNaiveBayesClassifier(naiveBayesClassifier, Xtest, yTest):
    print("Accuracy on Xtest:", naiveBayesClassifier.score(Xtest, yTest))

def visualizeHeatMapConfusionMatrix(naiveBayesClassifier, Xtest, yTest):
    # make predictions on the testing set
    y_pred = naiveBayesClassifier.predict(Xtest)

    # create a confusion matrix
    cm = confusion_matrix(yTest, y_pred)

    # plot the confusion matrix using a heatmap
    sns.heatmap(cm, annot=True, cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

def getNaiveBayesClassifier():
    filePathNaiveBayesClassifier = join(dirname(abspath(__file__)), "serializedObjects/naiveBayesClassifier.pickle")

    if isfile(filePathNaiveBayesClassifier):
        with open(filePathNaiveBayesClassifier, "rb") as f:
            naiveBayesClassifier = pickle.load(f)
    else:
        print("Creazione Naive Bayes classifier")
        naiveBayesClassifier = MultinomialNB(alpha=3, force_alpha=True, fit_prior=True)
        Xtrain, yTrain, Xtest, yTest = getXtrainYTrainXtestYTest()
        naiveBayesClassifier.fit(Xtrain, yTrain)

        with open(filePathNaiveBayesClassifier, "wb") as f:
            pickle.dump(naiveBayesClassifier, f)
        
        #getAccuracyNaiveBayesClassifier(naiveBayesClassifier, Xtest, yTest)
        #visualizeHeatMapConfusionMatrix(naiveBayesClassifier, Xtest, yTest)
        #for score in getModelScores(yTest, naiveBayesClassifier.predict(Xtest)):
        #    print (score)
        #    print()

    return naiveBayesClassifier
