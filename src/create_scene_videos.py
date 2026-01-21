import os
import json
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip

SCENES_JSON = "output/scenes_with_audio.json"
IMAGE_DIR = "all_images"
AUDIO_DIR = "audio"
OUTPUT_DIR = "output/scene_videos"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(SCENES_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

#  Your JSON: {"Scenes": [ ... ]}
scenes = data["Scenes"]

for scene in scenes:
    # scene_id is INT → convert to zero-padded string
    scene_num = int(scene["scene_id"])
    scene_id = f"scene_{scene_num:02d}"

    image_path = os.path.join(IMAGE_DIR, f"{scene_id}.png")

    # audio_file already contains correct path
    audio_path = scene["audio_file"].replace("\\", "/")

    output_path = os.path.join(OUTPUT_DIR, f"{scene_id}.mp4")

    if not os.path.exists(image_path):
        print(f" Missing image: {image_path}")
        continue

    if not os.path.exists(audio_path):
        print(f" Missing audio: {audio_path}")
        continue

    print(f" Rendering {scene_id}")

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    clip = (
        ImageClip(image_path)
        .with_duration(duration)
        .with_audio(audio)
    )

    final = CompositeVideoClip([clip])

    final.write_videofile(
    output_path,
    fps=24,
    codec="libx264",
    audio=True,                 # 🔥 REQUIRED
    audio_codec="aac",          # 🔥 REQUIRED
    temp_audiofile="temp.m4a",  # 🔥 IMPORTANT for Windows
    remove_temp=True,
    preset="medium"
)

    final.close()
    audio.close()

    print(f" Created {scene_id}")
