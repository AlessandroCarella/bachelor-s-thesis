import re
from os.path import join, splitext, basename, dirname
import os
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def find_trend(list_data):
    x = np.arange(len(list_data)).reshape(-1, 1)
    y = np.array(list_data).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, y)

    trend = 'unknown'
    if model.coef_ > 0:
        trend = 'positive'
    elif model.coef_ < 0:
        trend = 'negative'
        # Extrapolate to find the x-value where y = 0 (intersects y-axis)
        x_intercept = int(-model.intercept_ / model.coef_)
        num_points_needed = max(0, x_intercept - len(list_data))

        return num_points_needed

    return "Cannot determine the trend"

def positiveIn (list_data):
    for elem in list_data:
        if elem >= 0:
            return True
    return False

def generateValues (data):
    # Reshape the data for linear regression
    x = np.arange(len(data)).reshape(-1, 1)
    y = np.array(data)

    # Fit linear regression model
    regression_model = LinearRegression()
    regression_model.fit(x, y)

    # Generate next 1000 values
    next_1000_values = []
    next_1000_value_from_first_negative = []
    last_index = len(data) - 1

    for i in range(last_index + 1, last_index + 1001):
        next_value = regression_model.predict([[i]])
        
        if positiveIn(next_1000_value_from_first_negative):
            next_1000_values.extend(next_1000_value_from_first_negative)

        if  next_value[0] >= 0 and len (next_1000_value_from_first_negative) == 0:  # Check if the value is non-negative
            next_1000_values.append(next_value[0])
        else:
            next_1000_value_from_first_negative.append(next_value[0])
    
    if len (next_1000_values) == 1000:
        next_1000_values.extend (generateValues (next_1000_values)[0])


    return next_1000_values, len (next_1000_values)

def getOutFilesInFolder ():
    folder_path = os.getcwd()  # Get the current working directory

    return [join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".out")]

def getListOfNewtransitionsNumbers (filePath):
    # Read the file
    with open(filePath, 'r') as file:
        content = file.read()

    # Extract the newTransitions using regular expressions
    new_transitions = re.findall(r'NewTransitions:\s*(\.{100,})', content)

    # Get the number of newTransitions for each case
    num_new_transitions = [len(transition) for transition in new_transitions]

    return num_new_transitions

moodsNewTransitionsNums = {}
for file in getOutFilesInFolder ():
    moodsNewTransitionsNums[splitext(basename(file))[0]] = getListOfNewtransitionsNumbers(file)

for key, value in moodsNewTransitionsNums.items():
    #additional_points = find_trend (value)
    #print("Per il mood " + key + " è stato calcolato che potrebbero essere necessari altri " + str(additional_points) + " video o più.")
    generatedValues, numAddedValues = generateValues (value)
    print ("Valori precedenti")    
    print (value)
    print ("Valori successivi per il mood " + key)
    print (generatedValues)
    value.extend (generatedValues)

    # Generate x-axis values as the indices of the float_values list
    x = range(len(value))

    plt.subplots(figsize=(19.2, 10.8))
    
    # Plot the float_values against the indices
    plt.plot(x, value)

    plt.title(key + " prediction values")
    plt.xlabel("Cases")
    plt.ylabel("Count")
    
    # Save the image in the same folder as the input file
    plt.savefig(join(dirname(__file__), "graphs", "line graphs", key + " prediction values.png"), dpi=200)  # Set dpi to adjust resolution
    plt.close()

