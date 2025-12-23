#!/bin/bash

TIMESTAMP="${2:-3}"
OUTPUT_DIR="${HOME}/Pictures/wallpapersmpvpaper"
VIDEO_URL="https://youtu.be/pUEWTIciMZQ?si=p_iZryHr800j06y2"

mpv --no-audio \
    --start="$TIMESTAMP" \
    --frames=1 \
    --vo=image \
    --vo-image-format=png \
    --vo-image-outdir="$OUTPUT_DIR" \
    "$VIDEO_URL"
SCREENSHOT=$(ls -t "$OUTPUT_DIR"/*.png 2>/dev/null | head -n1)
echo "outout-$SCREENSHOT"