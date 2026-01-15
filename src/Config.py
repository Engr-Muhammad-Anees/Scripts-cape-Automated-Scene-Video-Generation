import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Hugging Face Model
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

# Output settings
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024

# Rate limit safety
SLEEP_BETWEEN_REQUESTS = 8  # seconds (important for free tier)

# Paths
PROMPT_FILE = BASE_DIR / "output" / "image_prompts.json"
OUTPUT_DIR = BASE_DIR / "all_images"
LOG_FILE = BASE_DIR / "logs" / "generation.log"
