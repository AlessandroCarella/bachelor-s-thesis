import os
import pandas as pd 

def fixFilePath (input_path):
    # Remove the "frame n" part from the path
    filename = os.path.basename(input_path)
    filename_without_frame = os.path.splitext(filename)[0].split('frame')[0].strip()

    # Get the directory of the input path
    directory = os.path.dirname(input_path)

    # Get the file extension from the original path
    file_extension = os.path.splitext(input_path)[1]

    # Create the output path
    output_path = os.path.join(directory, filename_without_frame + file_extension)

    return output_path

def extract_video_identifier(path):
    return os.path.dirname(path)

def removeDuplicatesInputFile(dataset):
    # Add a new column to the dataframe to store the video identifier
    dataset['video_identifier'] = dataset['input'].apply(extract_video_identifier)

    # Sort the dataframe by the video identifier and any other relevant sorting columns
    dataset = dataset.sort_values(by=['video_identifier'])

    # Drop the duplicate rows, keeping only the first occurrence (which corresponds to "frame 0")
    dataset = dataset.drop_duplicates(subset='video_identifier', keep='first')

    # Remove the additional column
    dataset = dataset.drop(columns=['video_identifier'])

    return dataset

def getUniqueValuesNoStudentEngagementDataset (df):
    #find the values the label column can have
    uniqueValues = list(df['label'].unique())
    # remove the student engagement dataset only values
    uniqueValues.pop (uniqueValues.index ("drowsy"))
    uniqueValues.pop (uniqueValues.index ("looking away"))
    
    return uniqueValues

def removeMatchingSamplesStudentEngagementDataset (df, uniqueValues):
    # create empty subdataset
    subdataset = pd.DataFrame()

    for value in uniqueValues:
        #get the samples for each value of the label column in the original dataset
        filtered_data = df[df['label'] == value]
        
        # Remove rows from the student engagement dataset
        sampled_data = filtered_data[~filtered_data['input'].str.contains('Student-engagement-dataset')]
        
        # Concatenate the sampled data for each unique value
        subdataset = pd.concat([subdataset, sampled_data])
    
    return subdataset

def findLowerCountLabelClass (df):
    #find the label value with less samples
    lowerCount = 9999999
    for value, count in df['label'].value_counts().items():
        if count < lowerCount:
            lowerCount = count
    
    return lowerCount

def getDfWithLowerCountLabelClass (df, uniqueValues):
    # create empty subdataset
    subdataset = pd.DataFrame()  # Initialize an empty DataFrame
    for value in uniqueValues:
        subset = df[df["label"] == value]
        # Take a random sample of lowercount rows
        sampled_data = subset.sample(n=findLowerCountLabelClass(df), random_state=69)  # Adjust the random_state if needed

        # Concatenate the sampled data for each unique value
        subdataset = pd.concat([subdataset, sampled_data])
    
    return subdataset

def getEqualPathsAndLabelsFromDAiSEE ():
    # Load your data into a pandas DataFrame
    df = pd.read_csv(r'C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\final analysis\DAiSEE and student engagement dataset clean.csv')

    uniqueValues = getUniqueValuesNoStudentEngagementDataset(df)
    df = removeDuplicatesInputFile(removeMatchingSamplesStudentEngagementDataset(df, uniqueValues))
    
    df = getDfWithLowerCountLabelClass(df, uniqueValues)

    pathsAndLabels = {fixFilePath(key): value for key, value in zip(df["input"].tolist(), df["label"].tolist())}

    #save on pickle
    import pickle
    with open (r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\richiesta professore\pathsAndLabels.pickle", "wb") as f:
        pickle.dump (pathsAndLabels, f)
