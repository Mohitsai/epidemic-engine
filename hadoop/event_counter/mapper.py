#!/usr/bin/env python3
"""mapper.py"""

import sys

# input comes from STDIN (standard input)
# write some useful code here and print to STDOUT

firstlineflag = True
for line in sys.stdin:
    if firstlineflag:
        firstlineflag = False
        continue
    columns = line.strip().split(',') # Split on delimiter
    try:
        print("{}\t1".format(columns[1])) # Eventtype 1
    except:
        pass