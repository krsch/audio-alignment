#!/bin/sh
# <video1> <video2> <video-offset> <audio>
POS1="x=0:y=126"
POS2="x=1136:y=126"
BACKGROUND="RoleconVideoCover.jpg"
V1=$1
V2=$2
O2=$3
A=$4
OUT=$4
ffmpeg -c:v h264_cuvid -i $V1 -ss $O2 -c:v h264_cuvid -i $V2 -i $BACKGROUND -i $a -filter_complex "
[0:v] scale_npp=1136:851 [left];
[1:v] scale_npp=784:851 [right];
[2:v][left] overlay=$POS1 [back+left];
[back+left][right] overlay=$POS2:shortest=1 [out];
" -map out -map 3 -c:v h264_nvenc $OUT
