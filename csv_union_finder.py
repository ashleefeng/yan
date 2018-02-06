#! /usr/bin/env python

"""
Usage: ./csv_union_finder.py <Output Folder> <File 1> <File 2> ... <File n>
by Xinyu (Ashlee) Feng 2018.01.20
"""

import pandas as pd
import numpy as np
from scipy import stats
import sys

# read input files
outfolder = sys.argv[1]
print "Analyzing", outfolder
filenames = sys.argv[2:]
frames = []
for filename in filenames:
    frames.append(pd.read_csv(filename, header=5))

for i in range(len(frames)):
    frames[i] = frames[i].dropna(axis=0, thresh=2)

df = pd.concat(frames)

print "Printing initial file dimensions"

for dfi in frames:
    print dfi.shape
    
print "Before union", df.shape

df_union = df.drop_duplicates(subset=['x', 'y', 'z'])

print "After union", df_union.shape

# extract patient name

file = open(filenames[0])
i = 0
patient = ""
for line in file:
    if i == 1:
        patient = line.rstrip('\n').split(',')[1]
        break
    i += 1
file.close()

# compute stats
tokens = ['stats', patient]

for filename in filenames:
    filename_before_csv = filename.rstrip('.csv')
    tokens.append(filename_before_csv.split('_')[1])

outname =  '_'.join(tokens)
outname = outfolder + '/' + outname

results = pd.DataFrame(index=["VE_map", "AE_map", "ADC_map"], \
    columns=["mean", "median", "std", "5%", "95%", "skewness", "kurtosis","entropy", "pixel_number"])

coi = ['VE_map', 'AE_map', 'ADC_map']
egi = df_union[coi]
egi_array = egi.values

results["mean"] = egi.mean(axis=0)
results["median"] = egi.median(axis=0)
results["std"] = egi.std(axis=0)
results["5%"] = np.percentile(egi_array, 5, axis=0)
results["95%"]= np.percentile(egi_array, 95, axis=0)
results["kurtosis"] = stats.kurtosis(egi_array)
results["skewness"] = stats.skew(egi_array)
results["entropy"] = stats.entropy(egi_array)

npixel = egi.shape[0]
results["pixel_number"] = [npixel,np.NaN,np.NaN]

print results

print outname
results.to_csv(outname+'.csv')


