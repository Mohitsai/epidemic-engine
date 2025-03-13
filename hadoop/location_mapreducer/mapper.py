#!/usr/bin/env python3
"""mapper_location.py"""

import sys

# input comes from STDIN (standard input)

firstlineflag = True
for line in sys.stdin:
    if firstlineflag:
        firstlineflag = False
        continue
    columns = line.strip().split(',') # Split on delimiter
    try:
        print("{}\t1".format(columns[3])) # Location as key, count as 1
    except:
        pass
