import os
from os.path import join, isdir, isfile, abspath, dirname, sep, basename, splitext
import json
import pandas as pd
from tqdm import tqdm
import csv

df = pd.read_csv("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE and student engagement dataset.csv")

df = df.dropna(subset=['naturalLanguageDescription'])
df = df.dropna(subset=['AU01'])

df.to_csv("C:/Users/Alessandro/Desktop/bachelor-s-thesis/src/final analysis/DAiSEE and student engagement dataset clean.csv", index=False)