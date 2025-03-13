#!/usr/bin/env python3
"""reducer.py"""
import sys
# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

event_type_freq = {}

for line in sys.stdin:
    etype, count = line.strip().split('\t')
    try:
        event_type_freq[etype] = event_type_freq.get(etype, 0) + int(count)
    except ValueError:
        pass

# output to STDOUT
for etype, count  in event_type_freq.items():
    print("{}\t{}".format(etype, count))