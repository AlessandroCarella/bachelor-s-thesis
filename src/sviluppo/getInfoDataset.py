import pandas as pd

df = pd.read_csv('C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE and student engagement dataset.csv')

print (df['label'].value_counts())
print (df.shape)

nullVals = df.isnull()

print("Numero di valori nulli per ogni colonna:")
print(nullVals.sum())

"""print("\nRow numbers where null values occur:")
for column in nullVals.columns:
    rows = nullVals[nullVals[column] == True].index.tolist()
    if rows:
        print(f"{column}: {rows}")"""