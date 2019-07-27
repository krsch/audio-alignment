#!/usr/bin/env python3

import subprocess
import sys
import csv

def time_diff(end, start):
    end = list(map(int, end.split(":")))
    start = list(map(int, start.split(":")))
    return str(end[0]*60+end[1] - start[0]*60 - start[1])

def parse_options():
    movie = sys.argv[1]
    # audio = sys.argv[2]
    with open(sys.argv[2], newline='') as csvfile:
        times = list(csv.reader(csvfile))
    times = map(lambda t: (t[0], time_diff(t[1], t[0])), times)
    return (movie, times)

if __name__ == '__main__':
    (filename, times) = parse_options()
    split_cmd = []
    for n, time in enumerate(times):
        split_str = ["ffmpeg", "-v", "error",
                "-c:v", "h264_cuvid",
                "-accurate_seek",
                "-i", filename,
                "-ss", time[0], "-t", time[1],
                # "-ss", time[0], "-t", time[1],
                # "-i", audio,
                # "-shortest", "-map", "0", "-map", "1",
                "-c:v", "h264_nvenc", "-y",
                "-vf", "drawtext=text='" + filename[-5] + "\\:' %{pts} (%{n}):fontsize=60:fontcolor=white",
                filename[:-4] + "-" + str(n) + "." + filename[-3:]]
        print("About to run: "+ ' '.join(split_cmd+split_str))
        subprocess.run(split_cmd+split_str)
