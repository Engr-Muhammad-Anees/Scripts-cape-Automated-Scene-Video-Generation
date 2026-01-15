import os
import json
import logging


def load_script(file_path: str) -> str:
    if not os.path.exists(file_path):
        logging.error(f"Script file not found: {file_path}")
        raise FileNotFoundError(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        logging.warning("Script file is empty")

    return content


def save_json(file_path: str, data) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logging.info(f"Saved JSON → {file_path}")
