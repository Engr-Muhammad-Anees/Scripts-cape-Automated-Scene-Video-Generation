# main.py
import logging
import os
from dotenv import load_dotenv

# Import from your package
from src.utils import load_script, save_json
from src.analyzer import ScriptAnalyzer

def main():
    """
    Entry point for the Script Analyzer pipeline.

    Responsibilities:
    - Load environment variables
    - Read the input script file
    - Send the script to the ScriptAnalyzer (LLM-based)
    - Save the structured JSON output
    """

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    # Load environment variables from .env
    load_dotenv()

    # Define input/output paths
    script_path = "input/script"
    output_path = "output/scenes.json"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Step 1: Load the script
    try:
        script_text = load_script(script_path)
        logging.info(f"Loaded script: {script_path}")
    except FileNotFoundError as e:
        logging.error(e)
        return

    # Step 2: Initialize the ScriptAnalyzer
    analyzer = ScriptAnalyzer(model="allenai/molmo-2-8b:free")

    # Step 3: Analyze script
    result = analyzer.analyze(script_text, strategy="costar")

    # Step 4: Save output
    if result and "Scenes" in result and result["Scenes"]:
        save_json(output_path, result)
        logging.info(f"Scene extraction complete. Saved to: {output_path}")
    else:
        logging.error("No scenes were extracted. Check logs for details.")


if __name__ == "__main__":
    main()
