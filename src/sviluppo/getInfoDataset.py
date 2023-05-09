import pandas as pd
import matplotlib.pyplot as plt

def getNumberOfNullValuesForEachAU ():
    df = pd.read_csv('C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE and student engagement df.csv')

    print (df['label'].value_counts())
    print (df.shape)

    nullVals = df.isnull()

    print("Numero di valori nulli per ogni colonna:")
    print(nullVals.sum())

    print("\nRow numbers where null values occur:")
    for column in nullVals.columns:
        rows = nullVals[nullVals[column] == True].index.tolist()
        if rows:
            print(f"{column}: {rows}")

def getNumberOfValuesForEachLabel ():
    # Load your data into a pandas DataFrame
    df = pd.read_csv(r'C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\final analysis\DAiSEE and student engagement dataset clean.csv')

    # Replace 'my_column_name' with the name of the column you want to count values for
    value_counts = df['label'].value_counts()

    print(value_counts)

def visualizeDataFrameChart (df):
    # Count the number of samples for each value in a column
    counts = df['label'].value_counts()

    # Create a pie chart
    counts.plot(kind='pie')
    plt.title('Pie chart of counts for label')
    plt.show()

    # Create a bar chart
    counts.plot(kind='bar')
    plt.title('Bar chart of counts for label')
    plt.show()

def visualizeFeaturesImportances(rfc_model, X):
    # Generate pie chart
    ax = (pd.Series(rfc_model.feature_importances_, index=X.columns)
            .nlargest(10)
            .plot(kind='pie', figsize=(6, 6), autopct='%1.1f%%')
            .invert_yaxis())

    # Set plot properties
    plt.title("Top features derived by Random Forest")
    plt.ylabel("")
    plt.show()
    plt.clf()