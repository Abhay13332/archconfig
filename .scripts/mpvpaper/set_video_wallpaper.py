#!/usr/bin/env python3
import sys
import subprocess
import time
import os
from pathlib import Path
from datetime import datetime

def run_command(cmd, shell=False):
    """Utility to run a command and capture output."""
    try:
        return subprocess.run(cmd, shell=shell, check=False, capture_output=True, text=True)
    except Exception as e:
        print(f"Error executing command: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: set_video_wallpaper.py <VIDEO_FILE> [TIMESTAMP]")
        sys.exit(1)

    video_input = sys.argv[1]
    if video_input.startswith(("http://", "https://")):
        video_file = video_input
    else:
        video_file = str(Path(video_input).resolve())
    timestamp = sys.argv[2] if len(sys.argv) > 2 else "3"
    
    output_dir = Path.home() / "Pictures/wallpapersmpvpaper"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"wallpaper_{timestamp_str}.png"

    print(f"Extracting frame at {timestamp} seconds...")
    
    # mpv extraction
    extract_cmd = [
        "mpv", "--no-audio",
        f"--start={timestamp}",
        "--frames=1",
        "--vo=image",
        "--vo-image-format=png",
        f"--vo-image-outdir={output_dir}",
        str(video_file)
    ]
    subprocess.run(extract_cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Find the latest screenshot and move it to the output file
    screenshots = sorted(output_dir.glob("*.png"), key=os.path.getmtime, reverse=True)
    if screenshots:
        screenshot = screenshots[0]
        screenshot.rename(output_file)
    else:
        print("Failed to extract frame.")
        # We continue anyway if the video exists, as mpvpaper might still work
        # but output_file might be missing. In the original script, it proceeded.
    
    socket_path = "/tmp/mpv-socket"
    
    # Check if mpvpaper is already running with IPC socket
    res = run_command(["ss", "-xln"])
    if res and socket_path in res.stdout:
        print("mpvpaper already running, changing video...")
    else:
        run_command(["pkill", "mpvpaper"])
        print("Starting mpvpaper...")
        # Note: Using eDP-1 as per original script
        mpvshaderopts= '"~~/shaders/Anime4K_Clamp_Highlights.glsl:~~/shaders/Anime4K_Restore_CNN_VL.glsl:~~/shaders/Anime4K_Upscale_CNN_x2_VL.glsl:~~/shaders/Anime4K_AutoDownscalePre_x2.glsl:~~/shaders/Anime4K_AutoDownscalePre_x4.glsl:~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"'
        mpvpaper_opts = f"video-aspect-override=16:9 --panscan=1.0 --hwdec=nvdec --vo=gpu --loop --no-audio --input-ipc-server={socket_path} --glsl-shaders={mpvshaderopts}"
        mpvpaper_cmd = [
            "mpvpaper", "-o", mpvpaper_opts, "eDP-1", str(output_file)
        ]
        subprocess.Popen(mpvpaper_cmd)
        time.sleep(2)

    # Load the actual video via IPC
    print(f"Loading video: {video_file}")
    socat_cmd = f"echo 'loadfile \"{video_file}\" replace' | socat - {socket_path}"
    subprocess.run(socat_cmd, shell=True)

    print("Setting wallpaper with caelestia...")
    run_command(["caelestia", "wallpaper", "-f", str(output_file)])
    
    time.sleep(2)
    run_command(["hyprctl", "dispatch", "exec", "pkill awww-daemon"])

if __name__ == "__main__":
    main()
