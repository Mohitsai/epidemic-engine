#!/usr/bin/env python3
"""reducer_location.py"""

import sys

# input comes from STDIN (standard input)

location_freq = {}

for line in sys.stdin:
    location, count = line.strip().split('\t')
    try:
        location_freq[location] = location_freq.get(location, 0) + int(count)
    except ValueError:
        pass

# output to STDOUT
for location, count in location_freq.items():
    print("{}\t{}".format(location, count))
