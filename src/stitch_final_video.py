import os
import subprocess

SCENE_VIDEO_DIR = "output/scene_videos_fixed"
SUBTITLE_FILE = "output/subtitles2.srt"
FINAL_DIR = "output/final_video2_animation"
FINAL_VIDEO = os.path.join(FINAL_DIR, "final2.mp4")
CONCAT_FILE = "scene_list2.txt"

os.makedirs(FINAL_DIR, exist_ok=True)

# Create FFmpeg concat file (ordered)
videos = sorted(
    os.listdir(SCENE_VIDEO_DIR),
    key=lambda x: int(x.split("_")[-1].split(".")[0])
)

with open(CONCAT_FILE, "w", encoding="utf-8") as f:
    for video in videos:
        if video.endswith(".mp4"):
            video_path = os.path.join(SCENE_VIDEO_DIR, video).replace("\\", "/")
            f.write(f"file '{video_path}'\n")

print("scene_list.txt created")

# Escape subtitle path
subtitle_path = SUBTITLE_FILE.replace("\\", "/")

cmd = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", CONCAT_FILE,
    "-vf", f"subtitles='{subtitle_path}'",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-movflags", "+faststart",
    FINAL_VIDEO
]

subprocess.run(cmd, check=True)

print(" Final video created successfully:", FINAL_VIDEO)

