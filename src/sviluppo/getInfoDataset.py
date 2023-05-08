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

def visualizeDataFrameChart (df):
    # Count the number of samples for each value in a column
    counts = df['label'].value_counts()

    # Create a pie chart
    counts.plot(kind='pie')
    plt.title('Pie chart of counts for column_name')
    plt.show()

    # Create a bar chart
    counts.plot(kind='bar')
    plt.title('Bar chart of counts for column_name')
    plt.show()
