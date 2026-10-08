#!/bin/bash
# Owner photos from the Google Business Profile (used with the owner's permission).
# Blur number plates, apply one consistent grade, export WebP at web sizes.
# Usage: enhance.sh <srcDir with p3/p4/p5/p6.img> <outAssetsDir>
set -euo pipefail
I=$1; O=$2
# one look for every photo: lift shadows a touch, firmer contrast, cleaner whites, slight clarity
GRADE="eq=contrast=1.07:brightness=0.01:saturation=1.12:gamma=1.03,curves=all='0/0.02 0.25/0.24 0.75/0.78 1/1',unsharp=5:5:0.55:5:5:0.0"
blur() { # n x y w h  -> blur box n: [v(n-1)] -> [v(n)]
  echo "[v$(($1-1))]split[a$1][b$1];[b$1]crop=$4:$5:$2:$3,boxblur=lr=5:lp=3:cr=5:cp=3[bl$1];[a$1][bl$1]overlay=$2:$3[v$1]"; }
out() { # src name widths... (aspect kept)
  local src=$1 name=$2 pre=$3 last=$4; shift 4
  for w in "$@"; do
    ffmpeg -loglevel error -y -i "$I/$src" -filter_complex "[0]null[v0]$pre;[v$last]$GRADE,scale=$w:-2:flags=lanczos[o]" -map "[o]" -c:v libwebp -quality "${Q:-80}" "$O/$name-$w.webp"
  done; }
# interior: two parked cars' plates
out p6.img workshop ";$(blur 1 92 936 56 24);$(blur 2 640 970 66 24)" 2 1600
# facade: two front plates on the street
out p4.img facade ";$(blur 1 1316 754 36 22);$(blur 2 1606 756 32 22)" 2 900 1600
# alignment lift shots (no plates visible)
out p3.img align-911 "" 0 700 1100
ls -la "$O" | grep -E "workshop|facade|align"
# hero backgrounds (static): workshop floor for wide screens, RS 6 on the aligner for phones.
# They sit under a dark scrim, so a lower quality is invisible and keeps the first paint fast.
Q=60 out p6.img hero-workshop ";$(blur 1 92 936 56 24);$(blur 2 640 970 66 24)" 2 1280 1920
Q=60 out p5.img hero-rs6 "" 0 720 1080
