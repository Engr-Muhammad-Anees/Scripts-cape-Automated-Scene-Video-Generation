import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print(" Creating scene videos...")
subprocess.run(
    [sys.executable, os.path.join(BASE_DIR, "create_scene_videos.py")],
    check=True
)

print(" Concatenating scenes & adding subtitles...")
subprocess.run(
    [sys.executable, os.path.join(BASE_DIR, "concat_scenes.py")],
    check=True
)

print(" FULL PIPELINE COMPLETED SUCCESSFULLY")
