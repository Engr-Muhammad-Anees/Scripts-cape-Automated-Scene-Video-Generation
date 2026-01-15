import os
import re
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from json_repair import repair_json
from src.prompt import PromptBuilder

load_dotenv()
logging.basicConfig(level=logging.INFO)


class ScriptAnalyzer:
    """
    ScriptAnalyzer (Image-Based)
    ----------------------------
    Converts a script into visually rich, image-generation-ready scenes.

    Output Schema:
    {
        "Scenes": [
            {
                "scene_id": int,
                "description": str,
                "visual_focus": str,
                "duration": int
            }
        ]
    }
    """

    def __init__(self, model: str = "allenai/molmo-2-8b:free"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing in .env")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        self.model = model

    def analyze(self, script_text: str, strategy: str = "costar") -> dict:
        """
        Analyze script text and return image-ready scenes.
        """

        builder = PromptBuilder(strategy)
        messages = builder.build(script_text)

        logging.info("Extracting image-based scenes from script...")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2
            )
            result_text = response.choices[0].message.content
        except Exception as e:
            logging.error(f"LLM API call failed: {e}")
            return {"Scenes": []}

        # Clean LLM output
        result_text = result_text.strip()
        result_text = result_text.replace("\n", " ")
        result_text = re.sub(r'\]\s*\[', '], [', result_text)

        # Load JSON safely
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            try:
                fixed = repair_json(result_text)
                result = json.loads(fixed)
            except Exception as e:
                logging.error("JSON repair failed")
                logging.error(e)
                return {"Scenes": []}

        # Normalize structure
        if isinstance(result, list):
            result = {"Scenes": result}

        scenes = result.get("Scenes", [])
        if not isinstance(scenes, list):
            return {"Scenes": []}

        normalized = []
        seen_ids = set()

        for idx, scene in enumerate(scenes, start=1):
            scene_id = scene.get("scene_id", idx)
            if scene_id in seen_ids:
                continue
            seen_ids.add(scene_id)

            normalized.append({
                "scene_id": scene_id,
                "description": scene.get(
                    "description",
                    scene.get("text", "Visually rich cinematic scene")
                ),
                "visual_focus": scene.get(
                    "visual_focus",
                    "clear subject, cinematic lighting, realistic"
                )
            })

        return {"Scenes": normalized}
