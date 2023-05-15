import pandas as pd
import pickle
from os.path import join, isfile, abspath, dirname
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns
import matplotlib.pyplot as plt

from classifiers.randomForestClassifier import getXtrainYTrainXtestYTest, getModelScores

def visualizeHeatMapCorrelationMatrix(Xtrain):
    plt.clf()
    corr = Xtrain.corr()
    sns.heatmap(corr, cmap='coolwarm')
    plt.show()

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])

def getKnnClassifier():
    filePathKnnClassifier = join(dirname(abspath(__file__)), "serializedObjects/KnnClassifier.pickle")

    if isfile(filePathKnnClassifier):
        with open(filePathKnnClassifier, "rb") as f:
            KnnClassifier = pickle.load(f)
    else:
        nNeib = 1
        print("Creazione Knn classifier")
        KnnClassifier = KNeighborsClassifier(n_neighbors=nNeib)
        Xtrain, yTrain, Xtest, yTest = getXtrainYTrainXtestYTest()
        KnnClassifier.fit(Xtrain, yTrain)
        
        #for score in getModelScores(yTest, KnnClassifier.predict(Xtest)):
        #    print (score)
        #    print()
        #visualizeHeatMapCorrelationMatrix(Xtrain)

        with open(filePathKnnClassifier, "wb") as f:
            pickle.dump(KnnClassifier, f)

    return KnnClassifier


