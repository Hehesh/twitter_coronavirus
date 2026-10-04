#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'UnDotum'

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# get top 10, then sort low to high
items = sorted(
    counts[args.key].items(),
    key=lambda item: item[1],
    reverse=True
)[:10]

items = sorted(items, key=lambda item: item[1])

keys = [k for k, v in items]
values = [v for k, v in items]

# create plot
plt.bar(keys, values)
plt.xlabel('Key')
plt.ylabel('Count')
plt.title(args.key)

plt.tight_layout()

# output filename
safe_key = args.key.replace('#', '')
output_path = f'{os.path.basename(args.input_path)}_{safe_key}.png'

plt.savefig(output_path)
plt.close()

print('saving', output_path)
