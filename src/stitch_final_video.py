import os
import subprocess

SCENE_VIDEO_DIR = "output/scene_videos"
SUBTITLE_FILE = "output/subtitles.srt"
FINAL_DIR = "output/final_video"
FINAL_VIDEO = os.path.join(FINAL_DIR, "final.mp4")
CONCAT_FILE = "scene_list.txt"

os.makedirs(FINAL_DIR, exist_ok=True)

# Create FFmpeg concat file

with open(CONCAT_FILE, "w", encoding="utf-8") as f:
    for video in sorted(os.listdir(SCENE_VIDEO_DIR)):
        if video.endswith(".mp4"):
            video_path = os.path.join(SCENE_VIDEO_DIR, video).replace("\\", "/")
            f.write(f"file '{video_path}'\n")

print("scene_list.txt created")

# FFmpeg concat + subtitles

cmd = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", CONCAT_FILE,
    "-vf", f"subtitles={SUBTITLE_FILE}",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-movflags", "+faststart",
    FINAL_VIDEO
]

subprocess.run(cmd, check=True)

print(" Final video created successfully:", FINAL_VIDEO)
