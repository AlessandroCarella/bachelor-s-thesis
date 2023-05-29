import re
import matplotlib.pyplot as plt
from os.path import join, dirname

def barGraph (path):
    # Read the file and extract the relevant data
    with open(path, 'r') as file:
        content = file.read()

    # Extract the workflow name
    workflowName = re.search(r"New workflow : (.+)", content).group(1)

    # Extract the numbers of new tasks and new transitions for each case
    newTasks = re.findall(r'New Tasks: (\.{0,})', content)
    newTransitions = re.findall(r'NewTransitions: (\.{0,})', content)

    # Convert the extracted data to integer values
    newTasks = [len(tasks) for tasks in newTasks]
    newTransitions = [len(transitions) for transitions in newTransitions]

    # Set the figure size to 1920x1080 pixels
    fig, ax = plt.subplots(figsize=(19.2, 10.8))

    # Create the bar graph
    cases = range(1, len(newTasks) + 1)
    barWidth = 0.35

    ax.bar(cases, newTasks, width=barWidth, label='New Tasks')
    ax.bar([case + barWidth for case in cases], newTransitions, width=barWidth, label='New Transitions')

    ax.set_xlabel('Cases')
    ax.set_ylabel('Count')
    ax.set_title(workflowName)
    ax.legend()

    plt.tight_layout()

    # Save the image in the same folder as the input file
    plt.savefig(join(dirname(path), workflowName + '.png'), dpi=100)  # Set dpi to adjust resolution
    plt.close()

barGraph (r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\richiesta professore\createGraphs\bored.out")
barGraph (r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\richiesta professore\createGraphs\confused.out")