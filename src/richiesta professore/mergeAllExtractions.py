import os

def mergeTxtFiles(path):
    mergedContent = ""
    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt") and "merged" not in file.lower():
                filePath = os.path.join(root, file)
                with open(filePath, "r") as f:
                    mergedContent += f.read()
    
    mergedFilePath = os.path.join(path, "allMerged.txt")
    with open(mergedFilePath, "w") as f:  
        f.write(mergedContent)

def mergeTxtFilesSingleSubfolder(path):
    for root, dirs, files in os.walk(path):
        for subfolder in dirs:
            subfolderPath = os.path.join(root, subfolder)
            mergedFilePath = os.path.join(root, 'merged' + subfolder.capitalize() + '.txt')
            
            with open(mergedFilePath, 'w') as merged_file:
                for fileName in os.listdir(subfolderPath):
                    filePath = os.path.join(subfolderPath, fileName)
                    if os.path.isfile(filePath) and fileName.endswith('.txt'):
                        with open(filePath, 'r') as txt_file:
                            merged_file.write(txt_file.read())

folderPath = r"C:\Users\Alessandro\Desktop\a\src\richiesta professore\extractions"
mergeTxtFiles (folderPath)
mergeTxtFilesSingleSubfolder (folderPath)