import os
import json
import time
import logging
from huggingface_hub import InferenceClient
from PIL import Image

# ✅ CORRECT IMPORT
from src.Config import (
    MODEL_ID,
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    SLEEP_BETWEEN_REQUESTS,
    PROMPT_FILE,
    OUTPUT_DIR,
    LOG_FILE,
)

# -----------------------------
# Setup folders
# -----------------------------
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# -----------------------------
# Hugging Face Client
# -----------------------------
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found. Set environment variable.")

client = InferenceClient(
    model=MODEL_ID,
    token=HF_TOKEN
)

# -----------------------------
# Load prompts
# -----------------------------
if not PROMPT_FILE.exists():
    raise FileNotFoundError(f"Prompt file not found: {PROMPT_FILE}")

with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    scenes = json.load(f)

print(f"Total scenes found: {len(scenes)}")

# -----------------------------
# Generate images
# -----------------------------
for scene in scenes:
    scene_id = scene["scene_id"]
    prompt = scene["image_prompt"]

    output_path = OUTPUT_DIR / f"scene_{scene_id:02d}.png"

    if output_path.exists():
        print(f"Scene {scene_id} already exists. Skipping.")
        continue

    try:
        print(f"Generating Scene {scene_id}...")
        image = client.text_to_image(
            prompt,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT
        )

        image.save(output_path)
        logging.info(f"Scene {scene_id} generated successfully")

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    except Exception as e:
        logging.error(f"Scene {scene_id} failed: {str(e)}")
        print(f"Error in Scene {scene_id}: {e}")
        time.sleep(30)
