"""
improve_scenes.py
=================

Scene Enhancement Module for Automated Script-to-Video Pipeline

This module takes a basic `scenes.json` file generated from script parsing
and enriches each scene with audio-related metadata. The enhanced output
is suitable for downstream tasks such as:
- Text-to-Speech (TTS) generation
- Subtitle timing
- Background sound design
- Video composition

Input:
------
scenes.json
{
  "Scenes": [
    {
      "scene_id": 1,
      "description": "...",
      "visual_focus": "..."
    }
  ]
}

Output:
-------
scenes_enhanced.json
{
  "scenes": [
    {
      "scene_id": 1,
      "description": "...",
      "visual_focus": "...",
      "narration": "...",
      "audio_duration": 5.0,
      "voice_style": {...},
      "background_audio": "..."
    }
  ]
}
"""

import json
from typing import Dict, List


#: Average narration speed (words per second)
WORDS_PER_SECOND = 2.2

#: Default voice style used when no special rule is applied
DEFAULT_VOICE_STYLE = {
    "tone": "calm, narrative",
    "pace": "moderate",
    "emotion": "neutral"
}

#: Background audio presets inferred from scene context
BACKGROUND_AUDIO_PRESETS = {
    "village": "ambient village sounds, light wind",
    "field": "soft wind, distant birds",
    "indoor": "subtle room tone",
    "default": "soft ambient atmosphere"
}


def estimate_audio_duration(text: str, words_per_second: float = WORDS_PER_SECOND) -> float:
    """
    Estimate narration duration based on word count.

    Parameters
    ----------
    text : str
        Narration text.
    words_per_second : float
        Average speaking speed.

    Returns
    -------
    float
        Estimated duration in seconds.
    """
    word_count = len(text.split())
    return round(word_count / words_per_second, 2)


def generate_narration(description: str) -> str:
    """
    Generate an improved narration sentence from a scene description.

    This function currently performs lightweight rewriting.
    It can later be replaced with an LLM-based narration generator.

    Parameters
    ----------
    description : str
        Original scene description.

    Returns
    -------
    str
        Enhanced narration text.
    """
    narration = description.strip()

    if narration.endswith("."):
        narration = narration[:-1]

    return f"{narration}, unfolding quietly."


def infer_background_audio(description: str) -> str:
    """
    Infer background ambient audio based on scene description keywords.

    Parameters
    ----------
    description : str
        Scene description text.

    Returns
    -------
    str
        Background audio description.
    """
    desc_lower = description.lower()

    if "village" in desc_lower or "houses" in desc_lower:
        return BACKGROUND_AUDIO_PRESETS["village"]
    if "field" in desc_lower or "earth" in desc_lower:
        return BACKGROUND_AUDIO_PRESETS["field"]
    if "house" in desc_lower or "room" in desc_lower:
        return BACKGROUND_AUDIO_PRESETS["indoor"]

    return BACKGROUND_AUDIO_PRESETS["default"]


def infer_voice_style(scene_id: int) -> Dict[str, str]:
    """
    Assign voice style parameters based on scene order.

    Parameters
    ----------
    scene_id : int
        Scene identifier.

    Returns
    -------
    dict
        Voice style dictionary containing tone, pace, and emotion.
    """
    if scene_id == 1:
        return {
            "tone": "calm, contemplative",
            "pace": "slow",
            "emotion": "peaceful"
        }
    if scene_id == 2:
        return {
            "tone": "gentle, narrative",
            "pace": "moderate",
            "emotion": "empathetic"
        }

    return DEFAULT_VOICE_STYLE



def improve_scenes(input_path: str, output_path: str) -> None:
    """
    Enhance scenes with narration and audio metadata.

    Parameters
    ----------
    input_path : str
        Path to the input scenes JSON file.
    output_path : str
        Path to save the enhanced scenes JSON file.

    Returns
    -------
    None
    """
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    enhanced_scenes: List[Dict] = []

    for scene in data["Scenes"]:
        narration = generate_narration(scene["description"])
        duration = estimate_audio_duration(narration)

        enhanced_scene = {
            "scene_id": scene["scene_id"],
            "description": scene["description"],
            "visual_focus": scene["visual_focus"],

            # Audio-related enhancements
            "narration": narration,
            "audio_duration": duration,
            "voice_style": infer_voice_style(scene["scene_id"]),
            "background_audio": infer_background_audio(scene["description"])
        }

        enhanced_scenes.append(enhanced_scene)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump({"scenes": enhanced_scenes}, file, indent=2)

    print(f"✔ Scene enhancement completed: {output_path}")


if __name__ == "__main__":
    improve_scenes(
        input_path="output/scenes.json",
        output_path="output/scenes_enhanced.json"
    )
