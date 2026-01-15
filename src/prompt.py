# src/prompt.py
import json

class PromptBuilder:
    """
    Builds structured prompts to convert a plain script
    into visually rich, image-generation-ready scenes.
    """

    def __init__(self, strategy: str = "costar"):
        self.strategy = strategy

    def build(self, script_text: str):
        """
        Returns a list of messages for LLM consumption,
        including system and user instructions.
        """

        # Example scene for reference
        example_scene = {
            "scene_id": 1,
            "description": "A small village at dawn with mist floating above quiet mud houses and empty streets.",
            "visual_focus": "Wide shot, village at sunrise, misty atmosphere, calm and quiet"
        }

        user_prompt = (
            "You are a cinematic scene breakdown expert.\n\n"

            "TASK:\n"
            "- Convert the script into structured image-generation scenes.\n\n"

            "STRICT RULES:\n"
            "- Output ONLY valid JSON\n"
            "- No explanations, no markdown\n"
            "- Each sentence = one scene\n"
            "- description max 15 words, concise and visual\n"
            "- visual_focus describes framing, camera, lighting, location, characters, mood\n\n"

            "OUTPUT FORMAT:\n"
            '{ "Scenes": [ { "scene_id": int, "description": str, "visual_focus": str } ] }\n\n'

            "EXAMPLE SCENE:\n"
            f"{json.dumps(example_scene, indent=2)}\n\n"

            "SCRIPT:\n"
            f"{script_text}"
        )

        return [
            {"role": "system", "content": get_system_message()["content"]},
            {"role": "user", "content": user_prompt}
        ]


def get_prompt(script_text: str, strategy: str = "costar"):
    """
    Helper function to generate LLM messages.
    """
    return PromptBuilder(strategy).build(script_text)


def get_system_message():
    """
    System instruction to enforce strict JSON-only output.
    """
    return {
        "role": "system",
        "content": (
            "You extract SHORT, VISUAL scenes from scripts for image generation. "
            "Output MUST be valid JSON only, following the specified format exactly. "
            "Each scene must have: scene_id, description, visual_focus."
        )
    }
