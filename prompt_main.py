# main_prompt.py
import json
import os
from src.prompt_generator import PromptGenerator

def main():
    os.makedirs("output", exist_ok=True)

    input_file = "output/scenes.json"

    with open(input_file, "r") as infile:
        data = json.load(infile)

    scenes = data.get("Scenes", [])
    generator = PromptGenerator()
    prompts_output = []

    for scene in scenes:
        prompt_text = generator.generate(scene)
        prompts_output.append({
            "scene_id": scene["scene_id"],
            "image_prompt": prompt_text
        })

    with open("output/image_prompts.json", "w") as outfile:
        json.dump(prompts_output, outfile, indent=2)

    print(f" Generated {len(prompts_output)} image prompts successfully")

if __name__ == "__main__":
    main()
