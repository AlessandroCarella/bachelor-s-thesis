import pandas as pd
from sklearn.model_selection import cross_validate
from os.path import join, abspath, dirname


from classifiers.randomForestClassifier import getRandomForestClassifier
from classifiers.KnnClassifier import getKnnClassifier
from classifiers.naiveBayesClassifier import getNaiveBayesClassifier
from classifiers.SVMclassifier import getSVMClassifier

def getDataframe() -> pd.DataFrame:
    DAiSEE = pd.read_csv ((join(dirname(abspath(__file__)), "../final analysis/DAiSEE and student engagement dataset clean sampled.csv")))
    return DAiSEE.drop(["input", "naturalLanguageDescription", "numLabel"], axis=1)

def getMetricsEmptyDict () -> dict:
    # Create a dictionary to store the metrics
    return {
        'Accuracy': [],
        'Precision': [],
        'Recall': [],
        'Balanced Accuracy': []
    }

def updateMetricsDict (metrics:dict , crossValidationResults: dict) -> dict:
    # Append the metrics to the respective lists
    metrics['Accuracy'].extend(crossValidationResults['test_accuracy'])
    metrics['Precision'].extend(crossValidationResults['test_precision_weighted'])
    metrics['Recall'].extend(crossValidationResults['test_recall_weighted'])
    metrics['Balanced Accuracy'].extend(crossValidationResults['test_balanced_accuracy'])

    return metrics

def saveOnFile (predictModelName: str, metrics:dict, meanMetrics:dict) -> None:
    # Write the results to the text file
    with open(((join(dirname(abspath(__file__)), "metrics_results " + predictModelName + ".txt"))), "w") as file:
        for metric, metricScores in metrics.items():
            file.write(f"{metric}:\n")
            for i, score in enumerate(metricScores):
                file.write(f"  Dataset {i+1}: {score}\n")
            file.write(f"Mean {metric}: {meanMetrics[metric]}\n\n")


def calculateMetricsWithCrossValidation(model: dict, predictModelName:str, X:pd.DataFrame, y:pd.DataFrame, numberOfCrossValidations:int) -> None:
    metrics = getMetricsEmptyDict ()
    
    updateMetricsDict (
        metrics, 
        # Perform k-fold cross-validation and calculate metrics
        cross_validate(model, X, y, cv=numberOfCrossValidations, n_jobs=-1, scoring=[
            'accuracy', 
            'precision_weighted', 
            'recall_weighted', 
            'balanced_accuracy'
            ])
    )

    saveOnFile (
        predictModelName, 
        metrics, 
        {   
            metric: sum(metricScores) / len(metricScores)
            for metric, metricScores in metrics.items()
        }
    )
    
def performanceAnalysis(numberOfCrossValidations:int):
    dataset = getDataframe()
    # Get the features (input) data from the dataset
    X = dataset.drop("label", axis=1)  # Assuming "label" is the target column
    
    # Get the target (label) data from the dataset
    y = dataset["label"]

    models = {
        "Random forest classifier": getRandomForestClassifier(),
        "K-nearest neighbors classifier": getKnnClassifier(),
        "Naive bayes classifier": getNaiveBayesClassifier(),
        "Support vector machine classifier": getSVMClassifier()
    }

    for modelName in models:
        calculateMetricsWithCrossValidation(models[modelName], modelName, X, y, numberOfCrossValidations)

performanceAnalysis ()