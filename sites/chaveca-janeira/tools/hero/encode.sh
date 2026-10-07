#!/bin/bash
# Encode rendered frames (f0000..f0239, 24 fps, loop-periodic) into the web hero files.
# Usage: encode.sh <landscapeFramesDir> <portraitFramesDir> <outAssetsDir>
set -euo pipefail
L=$1; P=$2; O=$3
LOOK="noise=alls=3:allf=t,vignette=PI/5"
enc() { ffmpeg -loglevel error -y -framerate 24 -i "$1/f%04d.png" -vf "scale=$2:flags=lanczos,$LOOK,format=yuv420p" \
  -c:v libx264 -profile:v high -preset slower -crf "$3" -g 48 -tune film -movflags +faststart -an "$O/$4"; }
enc "$L" 1920:1080 22 hero-1080.mp4
enc "$L" 1280:720 24 hero-720.mp4
enc "$P" 1080:1920 23 hero-portrait.mp4
ffmpeg -loglevel error -y -i "$L/f0000.png" -vf "scale=1920:1080:flags=lanczos,noise=alls=3,vignette=PI/5" -c:v libwebp -quality 78 "$O/hero-poster-1920.webp"
ffmpeg -loglevel error -y -i "$L/f0000.png" -vf "scale=1280:720:flags=lanczos,noise=alls=3,vignette=PI/5" -c:v libwebp -quality 76 "$O/hero-poster-1280.webp"
ffmpeg -loglevel error -y -i "$P/f0000.png" -vf "scale=720:1280:flags=lanczos,noise=alls=3,vignette=PI/5" -c:v libwebp -quality 76 "$O/hero-poster-portrait.webp"
ls -la "$O"/hero-*
# VP9 WebM fallbacks for browsers without H.264
encw() { ffmpeg -loglevel error -y -framerate 24 -i "$1/f%04d.png" -vf "scale=$2:flags=lanczos,$LOOK,format=yuv420p" \
  -c:v libvpx-vp9 -b:v 0 -crf "$3" -row-mt 1 -deadline good -cpu-used 2 -g 48 -an "$O/$4"; }
encw "$L" 1920:1080 36 hero-1080.webm
encw "$L" 1280:720 38 hero-720.webm
encw "$P" 1080:1920 37 hero-portrait.webm
ls -la "$O"/hero-*.webm
