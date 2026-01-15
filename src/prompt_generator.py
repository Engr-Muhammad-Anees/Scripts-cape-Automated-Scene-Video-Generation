# src/prompt_generator.py
from src.util_prompt import validate_scene

class PromptGenerator:
    def __init__(self):
        # global style for consistency (VERY IMPORTANT)
        self.global_style = (
            "cinematic storytelling, ultra realistic, consistent characters, "
            "natural proportions, no face distortion, sharp focus, film color grading"
        )

    def generate(self, scene):
        validate_scene(scene)

        scene_id = scene["scene_id"]
        description = scene["description"]
        visual_focus = scene["visual_focus"]

        prompt = (
            f"Scene {scene_id}: {description} "
            f"Visual composition: {visual_focus}. "
            f"Lighting is soft and cinematic, realistic shadows. "
            f"High detail, 4K quality. "
            f"{self.global_style}."
        )

        return prompt
