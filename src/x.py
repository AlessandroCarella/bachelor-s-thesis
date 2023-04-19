import json
import os
from os.path import join, isdir, isfile, abspath, dirname, splitext

with open (join(abspath("src/analysis"), "video analysis only AUs in images format analysis.json"), "r") as f:
    data = json.load (f)

print (len (data))