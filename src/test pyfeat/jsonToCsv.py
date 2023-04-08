import pandas as pd

df = pd.read_json (r"outputFix.json")

df.to_csv (r"outputFix.csv", index = None)