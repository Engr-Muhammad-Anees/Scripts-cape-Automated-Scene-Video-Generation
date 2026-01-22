import os
import json
import subprocess
import random

# PATHS 
SCENES_JSON = "output/scenes_with_audio.json"
IMAGE_DIR = "all_images"
OUTPUT_DIR = "output/scene_videos_fixed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# LOAD SCENES 
with open(SCENES_JSON, "r", encoding="utf-8") as f:
    scenes = json.load(f)["Scenes"]

# HELPERS 
def run(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f" FFmpeg failed: {e}")
        return False
    return True

def get_audio_duration(audio_path):
    if not os.path.exists(audio_path):
        return None
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    try:
        duration = float(subprocess.check_output(cmd).decode().strip())
        return max(duration, 0.1)  # prevent zero duration
    except Exception as e:
        print(f" Could not get duration for {audio_path}: {e}")
        return None

# EFFECTS 

def ken_burns(image, audio, output, duration):
    return [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", image,
        "-i", audio,
        "-filter_complex",
        (
            "[0:v]fps=30,scale=2400:2400,"
            "zoompan=z='min(1+on*0.0006,1.08)':"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            "s=1920x1080,"
            "fade=t=in:st=0:d=1,"
            f"fade=t=out:st={duration-1}:d=1[v]"
        ),
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        output
    ]

def slide_pan(image, audio, output, duration):
    total_frames = int(duration * 30)
    return [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", image,
        "-i", audio,
        "-filter_complex",
        (
            f"[0:v]fps=30,scale=2600:1460,zoompan=z=1:x='on*(iw-1920)/{total_frames}':y=0:"
            f"s=1920x1080,fade=t=in:st=0:d=1,fade=t=out:st={duration-1}:d=1[v]"
        ),
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        output
    ]

def rotate_zoom(image, audio, output, duration):
    return [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", image,
        "-i", audio,
        "-filter_complex",
        (
            "[0:v]fps=30,scale=2400:2400,"
            "rotate=0.01*sin(2*PI*on/150):c=black@0,"
            "crop=1920:1080,fade=t=in:st=0:d=1,"
            f"fade=t=out:st={duration-1}:d=1[v]"
        ),
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        output
    ]

def cinematic_overlay(image, audio, output, duration):
    return [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", image,
        "-i", audio,
        "-filter_complex",
        (
            "[0:v]fps=30,scale=2400:2400,zoompan="
            "z='min(1+on*0.0005,1.07)':"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            "s=1920x1080,drawbox=x=0:y=0:w=iw:h=ih:color=black@0.25:t=fill,"
            "fade=t=in:st=0:d=1,"
            f"fade=t=out:st={duration-1}:d=1[v]"
        ),
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest",
        output
    ]

# PROCESS 
effects = [ken_burns, slide_pan, rotate_zoom, cinematic_overlay]

for scene in scenes:
    scene_id = f"scene_{int(scene['scene_id']):02d}"

    image_path = os.path.join(IMAGE_DIR, f"{scene_id}.png")
    audio_path = scene["audio_file"].replace("\\", "/")
    output_path = os.path.join(OUTPUT_DIR, f"{scene_id}.mp4")

    if not os.path.exists(image_path):
        print(f" Missing image: {image_path}")
        continue

    if not os.path.exists(audio_path):
        print(f" Missing audio: {audio_path}")
        continue

    duration = get_audio_duration(audio_path)
    if duration is None or duration <= 0:
        print(f" Invalid audio duration for {scene_id}")
        continue

    effect = random.choice(effects)
    print(f" Rendering {scene_id} | Effect: {effect.__name__}")

    success = run(effect(image_path, audio_path, output_path, duration))
    if success:
        print(f" Created {output_path}")
    else:
        print(f" Failed {scene_id}, trying Ken Burns as fallback")
        # fallback to ken_burns if random effect fails
        run(ken_burns(image_path, audio_path, output_path, duration))
        print(f" Fallback done {output_path}")

print(" ALL SCENES ATTEMPTED")


