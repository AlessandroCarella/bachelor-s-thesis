import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

def parseNewSample(sample_str):
    sampleList = sample_str.split(',')
    sampleList = sampleList [:20]
    sample = [float(x) for x in sampleList]
    return pd.DataFrame([sample], columns=['AU01','AU02','AU04','AU05','AU06','AU07','AU09','AU10','AU11','AU12','AU14','AU15','AU17','AU20','AU23','AU24','AU25','AU26','AU28','AU43'])


# Load the dataset
df = pd.read_csv('C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE and student engagement dataset clean.csv')

# Split the dataset into features and target variable
y = df['label']
X = df.drop(["input","naturalLanguageDescription","label","numLabel"], axis=1)

# Split the dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the random forest classifier
rf = RandomForestClassifier(n_estimators=100, verbose=True)
rf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = rf.predict_proba(X_test)

with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/kek/randomForestClassifier.pickle", "wb") as f:
    pickle.dump (rf, f)

with open('C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/kek/predModel.pickle', 'wb') as f:
    pickle.dump(y_pred, f)


"""
with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/kek/randomForestClassifier.pickle", "rb") as f:
    rf = pickle.load(f)

with open('C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/kek/predModel.pickle', 'rb') as f:
    y_pred = pickle.load (f)




new_sample_pred = rf.predict_proba(parseNewSample (
    '0.4220679998,0.4336869121,0.2922944427,0.3457737565,0.164391011,0.0,0.2836986482,0.0111041386,0.4697553217,0.180129528,0.4512628019,0.5743202567,0.6343905926,0.0,0.6472659707,0.587274611,0.0063919784,0.3714916706,0.373039335,0.0215576794,C:/Users/Alessandro/Desktop/bachelor-s-thesis/datasets/Student-engagement-dataset/Engaged/confused/0100.jpg,"Lip Corner Depressor, using the muscles: Depressor Anguli Oris, with a value of 0.5743202567; Chin Raiser, using the muscles: Mentalis, with a value of 0.6343905926; Lip Tightener, using the muscles: Orbicularis Oris, with a value of 0.6472659707; Lip Pressor, using the muscles: Orbicularis Oris, with a value of 0.587274611; ",confused,0'
    ))

# Print the percentage of belonging of each label for the first sample in the testing set
for i, label in enumerate(rf.classes_):
    print("{}: {:.2f}%".format(label, new_sample_pred[0][i]*100))
    """