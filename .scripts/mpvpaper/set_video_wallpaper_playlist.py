#!/usr/bin/env python3
import sys
import subprocess
import time
import os
import hashlib
from pathlib import Path
from datetime import datetime

def run_command(cmd, shell=False, capture_output=True):
    """Utility to run a command and capture output."""
    try:
        return subprocess.run(cmd, shell=shell, check=False, capture_output=capture_output, text=True)
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: set_video_wallpaper_playlist.py <INPUT> [TIMESTAMP]")
        sys.exit(1)

    input_val = sys.argv[1]
    timestamp = sys.argv[2] if len(sys.argv) > 2 else "3"
    
    output_dir = Path.home() / "Pictures/wallpapersmpvpaper"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"wallpaper_{timestamp_str}.png"

    if input_val.startswith(("http://", "https://")):
        video_url = input_val
    else:
        video_url = str(Path(input_val).resolve())
    
    # Check if input is a YouTube playlist
    if "youtube.com" in input_val or "youtu.be" in input_val:
        print("Fetching playlist videos...")
        cache_dir = Path.home() / ".cache/mpvpaper"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique cache file per playlist using hash
        playlist_hash = hashlib.md5(input_val.encode()).hexdigest()
        cache_file = cache_dir / f"playlist_{playlist_hash}"
        
        # Get all video IDs using yt-dlp
        res = run_command(["yt-dlp", "--flat-playlist", "--get-id", input_val])
        if res and res.stdout.strip():
            video_ids = res.stdout.strip().split("\n")
            total_videos = len(video_ids)
            
            # Read current pointer, default to 0
            pointer = 0
            if cache_file.exists():
                try:
                    pointer = int(cache_file.read_text().strip())
                except ValueError:
                    pointer = 0
            
            # Get video at current pointer
            if pointer < total_videos:
                video_id = video_ids[pointer]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"Playing video {pointer + 1}/{total_videos}: {video_url}")
                
                # Increment pointer and wrap around
                pointer = (pointer + 1) % total_videos
                cache_file.write_text(str(pointer))
            else:
                print("Pointer out of range, resetting to 0.")
                cache_file.write_text("0")
        else:
            print("Failed to fetch playlist IDs or playlist is empty. Using input as is.")

    print(f"Extracting frame at {timestamp} seconds...")
    
    # mpv extraction
    extract_cmd = [
        "mpv", "--no-audio",
        f"--start={timestamp}",
        "--frames=1",
        "--vo=image",
        "--vo-image-format=png",
        f"--vo-image-outdir={output_dir}",
        video_url
    ]
    # We use stderr=DEVNULL to hide mpv's verbose output during extraction
    subprocess.run(extract_cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Find the latest screenshot and move it to the output file
    screenshots = sorted(output_dir.glob("*.png"), key=os.path.getmtime, reverse=True)
    if screenshots:
        screenshot = screenshots[0]
        screenshot.rename(output_file)
    
    socket_path = "/tmp/mpv-socket"
    
    # Check if mpvpaper is already running with IPC socket
    res = run_command(["ss", "-xln"])
    if not (res and socket_path in res.stdout):
        run_command(["pkill", "mpvpaper"])
        print("Starting mpvpaper...")
        mpvpaper_opts = f"video-aspect-override=16:9 --hwdec=nvdec --vo=gpu --panscan=1.0 --loop --no-audio --input-ipc-server={socket_path}"
        mpvpaper_cmd = [
            "mpvpaper", "-o", mpvpaper_opts, "eDP-1", str(output_file)
        ]
        subprocess.Popen(mpvpaper_cmd)
        time.sleep(2)
    else:
        print("mpvpaper already running, changing video...")

    # Load the actual video via IPC
    socat_cmd = f"echo 'loadfile \"{video_url}\" replace' | socat - {socket_path}"
    subprocess.run(socat_cmd, shell=True)

    print("Setting wallpaper with caelestia...")
    run_command(["caelestia", "wallpaper", "-f", str(output_file)])
    
    time.sleep(2)
    run_command(["hyprctl", "dispatch", "exec", "pkill awww-daemon"])

if __name__ == "__main__":
    main()
