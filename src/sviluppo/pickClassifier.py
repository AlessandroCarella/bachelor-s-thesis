
import tkinter as tk
import time
from collections import Counter

from randomForestClassifier import getRandomForestClassifier
from KnnClassifier import getKnnClassifier

def predictProba (chosenClassifier, classifierObj, input):
    """
    input:
    1 = random forest
    2 = knn
    """
    if chosenClassifier == 1:
        return classifierObj.predict_proba (input)
    elif chosenClassifier == 2:
        return classifierObj.predict (input)
    return None

def getClassifierObj (buttonLabel):
    """
    input:
    1 = random forest
    2 = knn
    """
    if buttonLabel == 1:
        return getRandomForestClassifier()
    elif buttonLabel == 2:
        return getKnnClassifier()
    return None

def getLabelsList ():
    return ['bored' 'confused' 'drowsy' 'engaged' 'frustrated' 'looking away']

    
def addToBestClassesLastMinute (bestClass, bestClassesLastMinute):
    bestClassesLastMinute[time.time()] = bestClass
    return bestClassesLastMinute

def removeOldKeys(bestClassesLastMinute):
    currentTime = time.time()
    oneMinuteAgo = currentTime - 60
    return {k:v for k,v in bestClassesLastMinute.items() if k > oneMinuteAgo}

def getMostFrequentMoodLastMinute (bestClassesLastMinute):
     # Count the number of occurrences of each value in the dictionary
    valueCounts = Counter(bestClassesLastMinute.values())

    # Get the value with the highest count
    mostFrequentValue, count = valueCounts.most_common(1)[0]

    return mostFrequentValue

def getPredictionTextRandomForestClassifier (prediction, timeDiff, bestClassesLastMinute):
    bestClass = ""
    maxProb = 0
    text = ""
    for i, label in enumerate(getLabelsList()):
        prob = prediction[0][i] * 100
        text += "{}: {:.2f}%\n".format(label, prob)
        if prob > maxProb:
            maxProb = prob
            bestClass = label

    bestClassesLastMinute = addToBestClassesLastMinute (bestClass, bestClassesLastMinute)
    bestClassesLastMinute = removeOldKeys(bestClassesLastMinute)
    
    return (
        "\n\n\n\n\nMood rilevato: " + bestClass + 
        "\n\nCon i valori:\n" + text + 
        "\n\n\nMood più frequente nell'ultimo minuto: " + getMostFrequentMoodLastMinute(bestClassesLastMinute) + 
        "\n" + "Temp dalla predizione precedente " + "{:.2f}".format(timeDiff)
    ), bestClassesLastMinute

def getPredictionTextKnnClassifier(prediction, timeDiff, bestClassesLastMinute):
    bestClassesLastMinute = addToBestClassesLastMinute (prediction, bestClassesLastMinute)
    bestClassesLastMinute = removeOldKeys(bestClassesLastMinute)
    
    return (
        "\n\n\n\n\nMood rilevato: " + prediction + 
        "\n\n\nMood più frequente nell'ultimo minuto: " + getMostFrequentMoodLastMinute(bestClassesLastMinute) + 
        "\n" + "Temp dalla predizione precedente " + "{:.2f}".format(timeDiff)
    ), bestClassesLastMinute

def getModelPredictionText (chosenClassifier, prediction, timeDiff, bestClassesLastMinute):
    """
    input:
    1 = random forest
    2 = knn
    """
    if chosenClassifier == 1:
        return getPredictionTextRandomForestClassifier(prediction, timeDiff, bestClassesLastMinute)
    elif chosenClassifier == 2:
        return getPredictionTextKnnClassifier(prediction, timeDiff, bestClassesLastMinute)
    return None

def onButtonClick(button_label, root):
    root._button_clicked = button_label # define _button_clicked attribute
    root.quit() # stop the mainloop

def onClose(root):
    root._button_clicked = None
    root.destroy()

def getGui(root):
    label = tk.Label(root, text="Select a classifier:", padx=10, pady=10)
    label.grid(row=0, column=0, columnspan=2)

    button1 = tk.Button(root, text="Random Forest classifier", padx=10, pady=10, command=lambda:onButtonClick(1, root))
    button2 = tk.Button(root, text="Knn classifier", padx=10, pady=10, command=lambda:onButtonClick(2, root))

    button1.grid(row=1, column=0, padx=10, pady=10)
    button2.grid(row=1, column=1, padx=10, pady=10)

    # Register a function to handle the "WM_DELETE_WINDOW" event
    root.protocol("WM_DELETE_WINDOW", lambda:onClose(root))

def pickClassifier(nTentative=0):
    """
    output:
    1 = random forest
    2 = knn
    """
    root = tk.Tk()
    root.title("Button Example")

    getGui(root)

    root._button_clicked = None # initialize _button_clicked attribute

    root.mainloop() # start the mainloop

    return root._button_clicked, getClassifierObj (root._button_clicked)