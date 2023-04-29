import os
from os.path import join, isdir, isfile, abspath, dirname, sep
import json
from tqdm import tqdm

from naturalLanguageDescriptionFromAU import getAUs, getPossibleAUsNames, getNaturalLanguageDescription

with open ("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/video analysis only AUs in images format analysis.json") as f:
    data = json.load(f)

AUs = getAUs()
possibleAUsNames = getPossibleAUsNames ()

outPath = "C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/analysis/video analysis only AUs in images format analysis with natural language description.json"

for i in tqdm(range(len(data))):
    sample = data [i]
    data [i]["naturalLanguageDescription"] = getNaturalLanguageDescription (sample, possibleAUsNames, AUs)

with open(outPath, "w") as f:
    tqdm(json.dump(data, f, indent=4), desc="Writing JSON data", total=len(data))