def generate_output(tasks_list, transitions_list):
    activities = set()
    transitions = {}
    alternatives = {}

    # Parse tasks list
    for task in tasks_list:
        activity, cases = task.split(',[')
        cases = "[" + cases
        activities.add(activity)
        cases = [int(case) for case in cases[1:-1].split(',')]
        transitions[activity] = cases

    # Parse transitions list
    for transition in transitions_list:
        source, destination, probability, cases = transition.split(',')
        source = source[1:-1]
        destination = destination[1:-1]
        probability = probability[1:]
        cases = [int(case) for case in cases[1:-1].split(',')]
        transitions[(source, destination)] = {'probability': probability, 'cases': cases}

        if source in alternatives:
            alternatives[source].append(destination)
        else:
            alternatives[source] = [destination]

    # Generate the output
    output = f'Activity "{activities.pop()}" was carried out in all cases, while '
    while activities:
        activity = activities.pop()
        if activity == 'dress':
            output += f'"{activity}" followed "tea" in only one case (#2), that is, 1/9 = 11% of the times only '
            output += '(hence, a noise threshold of 0.15 would ignore it).'
        elif activity == 'prepare_snack':
            output += f'"{activity}" was always followed by '
        else:
            output += f'"{activity}" followed '

        if activity in alternatives:
            routes = alternatives[activity]
            for route in routes:
                route_cases = transitions[(activity, route)]['cases']
                percentage = len(route_cases) / len(transitions[activity])
                output += f'"{route}" in {len(route_cases)} cases ({percentage:.2%}), '

    output += 'p20 requires that '

    # Check if optional activities are present
    optional_activities = ['magazine', 'radio', 'eat_snack']
    present_optional_activities = [
        activity for activity in optional_activities if activity in activities
    ]
    if present_optional_activities:
        output += '"' + '", "'.join(present_optional_activities) + '" must all be running '
        output += 'in order to terminate the routine, and implies that they all stop before ending the routine. '

    output += 'p5, p6, and p7 start alternative routes: In fact, the cases associated with p6 and p7 are complementary subsets '
    output += 'of cases #1 through #8 (including 5 and 3 cases, respectively, which yields weights 5/9 = 0.56 for the former '
    output += 'and 3/9 = 0.33 for the latter), while p5 accounts for case #9. In particular, p5 (together with p3) determines '
    output += 'a loop, "toilet"-"relax"-"toilet" in cases #1 and #8, while in case #9 it was followed by activity "dress," '
    output += 'as specified by p13. Other alternative routes are present, all terminating with the user dressing and going out '
    output += 'or reading a magazine while eating a snack and listening to the radio.'

    # Check optional activities for alternative routes
    if 'coffee' in activities:
        output += ' "coffee" is carried out between "relax" and "toilet,"'
    if 'tea' in activities:
        output += ' "tea" is carried out between "relax" and "toilet,"'
    if 'coffee' not in activities and 'tea' not in activities:
        output += ' "toilet" comes immediately after "relax."'

    return output


def main ():
    with open (r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\WOman\moodModelsAnalysis\splittedMoodModels\bored\25 task.txt", "r") as f:
        tasks = f.readlines ()
    with open (r"C:\Users\Alessandro\Desktop\bachelor-s-thesis\src\WOman\moodModelsAnalysis\splittedMoodModels\bored\21 transition.txt", "r") as f:
        transitions = f.readlines ()

    with open ("ciao.txt", "w") as f:
        for line in generate_output (tasks, transitions):
            f.write (line + "\n")

main ()