from os import listdir, makedirs
import shutil
import random
from os.path import join, dirname, abspath, isdir

def kFoldFilesAtPath (path, nFold):
    # Create a new folder called "folds" in the specified path
    folds_path = join(path, "folds")
    makedirs(folds_path, exist_ok=True)

    # Get a list of all the files in the path
    file_list = [file for file in listdir(path) if file != "folds"]
    random.shuffle(file_list)  # Randomize the order of files

    # Calculate the number of files per fold
    num_files = len(file_list)
    files_per_fold = num_files // nFold

    # Create the folds and distribute the files
    for fold in range(nFold):
        # Create a new fold folder
        fold_path = join(folds_path, f"fold_{fold + 1}")
        makedirs(fold_path, exist_ok=True)

        # Create the train and test subfolders within the fold folder
        train_path = join(fold_path, "train")
        test_path = join(fold_path, "test")
        makedirs(train_path, exist_ok=True)
        makedirs(test_path, exist_ok=True)

        # Determine the start and end indices for the files in the current fold
        start_index = fold * files_per_fold
        end_index = (fold + 1) * files_per_fold if fold < 9 else num_files

        # Distribute the files into the train and test folders
        for i, file_name in enumerate(file_list):
            file_path = join(path, file_name)
            destination_folder = train_path if start_index <= i < end_index else test_path
            shutil.copy(file_path, destination_folder)

def main (nFold):
    mainPath = (join(dirname(abspath(__file__)), "extractions"))
    for subpath in listdir(mainPath):
        if isdir(join(mainPath, subpath)):
            kFoldFilesAtPath (join(mainPath, subpath), nFold)

main (10)