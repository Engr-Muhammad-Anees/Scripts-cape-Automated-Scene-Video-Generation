import json
from datetime import timedelta


def format_srt_time(seconds: float) -> str:
    """
    Convert seconds to SRT time format: HH:MM:SS,mmm
    """
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    milliseconds = int((seconds - total_seconds) * 1000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def generate_srt_from_scenes(
    input_json: str,
    output_srt: str
):
    """
    Generate a valid SRT subtitle file from scenes JSON
    """
    # Load JSON data
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Get scenes (handle both uppercase and lowercase keys)
    scenes = data.get("Scenes") or data.get("scenes")
    if not scenes:
        raise ValueError("No scenes found in JSON")

    current_time = 0.0
    srt_blocks = []

    for index, scene in enumerate(scenes, start=1):
        # Get duration
        duration = scene.get("audio_duration")
        if not duration or duration <= 0:
            print(f" Warning: Scene {scene.get('scene_id', index)} has invalid duration, skipping...")
            continue

        # Get subtitle text (narration or description)
        subtitle_text = (
            scene.get("narration") or 
            scene.get("description") or 
            scene.get("text") or
            ""
        )
        
        # Clean and validate subtitle text
        subtitle_text = subtitle_text.strip()
        if not subtitle_text:
            print(f" Warning: Scene {scene.get('scene_id', index)} has no text, skipping...")
            continue

        # Calculate timestamps
        start_time = current_time
        end_time = start_time + duration

        # Build SRT block (each part on separate line)
        srt_blocks.append(f"{index}")
        srt_blocks.append(f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}")
        srt_blocks.append(subtitle_text)
        srt_blocks.append("")  # Blank line separator

        current_time = end_time

    # Write to file with proper line endings
    with open(output_srt, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(srt_blocks))

    print(f" Subtitles generated successfully → {output_srt}")
    print(f" Total subtitles: {len(srt_blocks) // 4}")


def validate_srt_file(srt_file: str):
    """
    Validate that the generated SRT file has correct format
    """
    with open(srt_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    lines = content.strip().split("\n")
    
    # Basic validation
    if not lines[0].isdigit():
        print(" ERROR: SRT must start with index number")
        return False
    
    if "-->" not in lines[1]:
        print(" ERROR: Second line must be timestamp")
        return False
    
    print(" SRT format appears valid")
    return True


if __name__ == "__main__":
    try:
        # Generate SRT
        generate_srt_from_scenes(
            input_json="output/scenes_with_audio.json",
            output_srt="output/subtitles.srt"
        )
        
        # Validate the output
        validate_srt_file("output/subtitles.srt")
        
    except FileNotFoundError as e:
        print(f" File not found: {e}")
    except json.JSONDecodeError as e:
        print(f" Invalid JSON format: {e}")
    except Exception as e:
        print(f" Error: {e}")