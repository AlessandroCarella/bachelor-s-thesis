from sklearn.metrics import balanced_accuracy_score
from os.path import join, abspath, dirname
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, balanced_accuracy_score
from sklearn.model_selection import KFold

from classifiers.SVMclassifier import getSVMClassifier

# Step 1: Split the dataset into features (X) and target variable (y)

def getDataframe() -> pd.DataFrame:
    DAiSEE = pd.read_csv ((join(dirname(abspath(__file__)), "../final analysis/DAiSEE and student engagement dataset clean sampled.csv")))
    return DAiSEE.drop(["input", "naturalLanguageDescription", "label"], axis=1)

dataset = getDataframe()

# Define the threshold for converting predictions into binary values
threshold = 0.00001

# Initialize lists to store the metrics for each fold
accuracy_scores = []
precision_scores = []
recall_scores = []
balanced_accuracy_scores = []

# Create a 33-fold cross-validator
kfold = KFold(n_splits=33)

# Perform cross-validation
for train_index, test_index in kfold.split(dataset):
    # Split the data into training and testing sets for the current fold
    df_train, df_test = dataset.iloc[train_index], dataset.iloc[test_index]
    
    # Separate the input features (X) and the target variable (y) for both the training and testing sets
    X_train, y_train = df_train.drop('numLabel', axis=1), df_train['numLabel']
    X_test, y_test = df_test.drop('numLabel', axis=1), df_test['numLabel']
    
    # Initialize and train the SVR classifier
    svr = getSVMClassifier()
    svr.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = svr.predict(X_test)
    
    # Convert predictions to binary values based on the threshold
    y_pred_binary = [1 if pred >= threshold else 0 for pred in y_pred]

    # Calculate metrics for the current fold
    accuracy = accuracy_score(y_test, y_pred_binary)
    precision = precision_score(y_test, y_pred_binary, average='weighted')
    recall = recall_score(y_test, y_pred_binary, average='weighted')
    balanced_accuracy = balanced_accuracy_score(y_test, y_pred_binary)
    
    # Append the metrics to the respective lists
    accuracy_scores.append(accuracy)
    precision_scores.append(precision)
    recall_scores.append(recall)
    balanced_accuracy_scores.append(balanced_accuracy)

# Calculate the mean of each metric
mean_accuracy = sum(accuracy_scores) / len(accuracy_scores)
mean_precision = sum(precision_scores) / len(precision_scores)
mean_recall = sum(recall_scores) / len(recall_scores)
mean_balanced_accuracy = sum(balanced_accuracy_scores) / len(balanced_accuracy_scores)

# Print the results
print("Accuracy:", mean_accuracy)
print("Weighted Precision:", mean_precision)
print("Weighted Recall:", mean_recall)
print("Balanced Accuracy:", mean_balanced_accuracy)

with open ("ciao.txt", "w") as f:
    f.write ("Accuracy:\n")
    for elem in accuracy_scores:
        f.write (str(round(elem * 100, 5)) + "\n")
    f.write ("Weighted Precision:\n")
    for elem in precision_scores:
        f.write (str(round(elem * 100, 5)) + "\n")
    f.write ("Weighted Recall:\n")
    for elem in recall_scores:
        f.write (str(round(elem * 100, 5)) + "\n")
    f.write ("Balanced Accuracy:\n")
    for elem in balanced_accuracy_scores:
        f.write (str(round(elem * 100, 5)) + "\n")
    f.write ("Means:")
    f.write ("Accuracy:" + str(round(mean_accuracy * 100, 5)) + "\n")
    f.write ("Weighted Precision:" + str(round(mean_precision * 100, 5)) + "\n")
    f.write ("Weighted Recall:" + str(round(mean_recall * 100, 5)) + "\n")
    f.write ("Balanced Accuracy:" + str(round(mean_balanced_accuracy * 100, 5)) + "\n")