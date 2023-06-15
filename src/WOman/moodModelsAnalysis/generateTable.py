"""
numero di task,
numero di transition, 
numero di eventi,
numero di attivita
"""
from os.path import join, dirname
from os import listdir
from tabulate import tabulate

def getNumberFromFile (filePath):
    with open (filePath) as f:
        n = f.readline ()
    return n.replace ("\n", "")

def getTasksAndTransitions (table):
    splittedMoodModelsFolderPath = join(dirname(__file__), "splittedMoodModels")
    for mood in listdir(splittedMoodModelsFolderPath):
        if mood != "results": #folder == one of the moods
            table[mood] = {}
            for file in listdir(join(splittedMoodModelsFolderPath, mood)):
                filePath = join(splittedMoodModelsFolderPath, mood, file)
                if file == "26 counter.txt":
                    table [mood]["tasksNumber"] = getNumberFromFile (filePath)
                elif file == "20 transition_counter.txt":
                    table [mood]["transitionsNumber"] = getNumberFromFile (filePath)
    return table

def getActivitesAndEvents (table):
    extractionsMoodsMergedFolderPath = join(dirname(__file__), "extractionsMoodsMerged")
    for file in listdir(extractionsMoodsMergedFolderPath):
        filePath = join (extractionsMoodsMergedFolderPath, file)
        with open (filePath) as f:
            fileLines = f.readlines ()

        eventCounter = 0
        activityCounter = 0
        for line in fileLines:
            if "begin_of_process" in line:
                eventCounter += 1
            elif "begin_of_activity" in line:
                activityCounter += 1
                eventCounter += 1

        mood = file.replace ("merged", "").replace (".txt", "").lower() 
        table [mood]["activitiesNumber"] = activityCounter
        table [mood]["eventsNumber"] = eventCounter
    return table

def tableToLatex (table):
    # Convert the dictionary to a list of lists
    table_data = []
    header = ['mood', 'activitiesNumber', 'eventsNumber', 'tasksNumber', 'transitionsNumber']
    table_data.append(header)
    for mood, values in table.items():
        row = [mood]
        for key in header[1:]:
            row.append(values[key])
        table_data.append(row)

    # Generate the LaTeX table
    tableLatex = tabulate(table_data, headers="firstrow", tablefmt="latex")

    # Save the LaTeX table to a file
    with open('table.tex', 'w') as file:
        file.write(tableLatex)


def main ():
    table = {}
    """
    mood key:
        taskNumber = subkey:value
        transitionNumber = subkey:value
        eventsNumber = subkey:value
        activitiesNumber = subkey:value
    """
    table = getTasksAndTransitions (table)
    table = getActivitesAndEvents (table)
    tableToLatex (table)

main ()