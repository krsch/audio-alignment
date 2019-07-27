#!/usr/bin/env python3

import subprocess
import sys
import csv

def time_diff(end, start):
    end = list(map(float, end.split(":")))
    start = list(map(float, start.split(":")))
    return str(end[0]*60+end[1] - start[0]*60 - start[1])

def parse_options():
    with open(sys.argv[1], newline='') as csvfile:
        times = list(csv.reader(csvfile))
    times = map(lambda t: (t[0], time_diff(t[1], t[0])), times)
    return times

if __name__ == '__main__':
    times = parse_options()
    print(sum([float(t[1]) for t in times]))
