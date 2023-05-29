import re
import matplotlib.pyplot as plt
from os.path import join, dirname, abspath, splitext
from os import listdir

def createLineGraph (path, identifier):
    # Read the file and extract the relevant data
    with open(path, 'r') as file:
        content = file.read()

    # Extract the workflow name
    workflowName = re.search(r"New workflow : (.+)", content).group(1)

    # Extract the numbers of new tasks and new transitions for each case
    data = re.findall(identifier + r': (\.{0,})', content)

    # Convert the extracted data to integer values
    data = [len(tasks) for tasks in data]

    # Set the figure size to 1920x1080 pixels
    fig, ax = plt.subplots(figsize=(19.2, 10.8))

    # Create the bar graph
    cases = range(1, len(data) + 1)
    barWidth = 0.35

    # Creazione del grafico a linee spezzate
    plt.plot(cases, data, marker='o', linestyle='-', color='b')

    # Personalizzazione del grafico
    plt.title(workflowName + " " + identifier)
    plt.xlabel("Cases")
    plt.ylabel("Count")
    
    # Save the image in the same folder as the input file
    plt.savefig(join(dirname(path), "graphs", "line graphs", workflowName + " " + identifier + '.png'), dpi=100)  # Set dpi to adjust resolution
    plt.close()

def createBarGraph (path, identifier):
    # Read the file and extract the relevant data
    with open(path, 'r') as file:
        content = file.read()

    # Extract the workflow name
    workflowName = re.search(r"New workflow : (.+)", content).group(1)

    # Extract the numbers of new tasks and new transitions for each case
    data = re.findall(identifier + r': (\.{0,})', content)

    # Convert the extracted data to integer values
    data = [len(tasks) for tasks in data]

    # Set the figure size to 1920x1080 pixels
    fig, ax = plt.subplots(figsize=(19.2, 10.8))

    # Create the bar graph
    cases = range(1, len(data) + 1)
    barWidth = 0.35

    ax.bar(cases, data, width=barWidth, label=identifier)

    ax.set_xlabel('Cases')
    ax.set_ylabel('Count')
    ax.set_title(workflowName + " " + identifier)
    ax.legend()

    plt.tight_layout()
    
    # Save the image in the same folder as the input file
    plt.savefig(join(dirname(path), "graphs", "bar graphs", workflowName + " " + identifier + '.png'), dpi=100)  # Set dpi to adjust resolution
    plt.close()

identifiers = [
    "New Tasks",
    "NewTransitions"
]
for file in listdir(dirname(abspath(__file__))):
    if splitext(file)[1] == ".out":
        outFile = join (dirname(abspath(__file__)), file)
        for identifier in identifiers:
            createBarGraph (outFile, identifier)
            createLineGraph (outFile, identifier)