import json

with open("output.json", "r") as f:
    data = json.loads(f.read())

output = []
for element in data:
    elem = {}
    for key, value in element.items():
        elem[key] = value["0"]
    output.append(elem) 

with open ("outputFix.json", "w") as file:
    file.write (json.dumps (output, indent=4))
