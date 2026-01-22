import json
from datetime import timedelta
import re


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


def split_into_phrases(text: str, max_words=7):
    """
    Split text into readable phrases
    """
    # Remove unwanted repetitive phrases
    REMOVE_PHRASES = [
        "unfolding quietly",
        "slowly unfolding",
        "fading into silence"
    ]
    for p in REMOVE_PHRASES:
        text = text.replace(p, "")

    text = text.strip()

    # Split by punctuation first
    chunks = re.split(r"[,.]", text)
    phrases = []

    for chunk in chunks:
        words = chunk.strip().split()
        if not words:
            continue

        # Further split long chunks
        for i in range(0, len(words), max_words):
            phrase = " ".join(words[i:i + max_words])
            phrases.append(phrase)

    return phrases


def generate_srt_from_scenes(input_json: str, output_srt: str):
    """
    Generate phrase-by-phrase SRT file from scenes JSON
    """
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    scenes = data.get("scenes") or data.get("Scenes")
    if not scenes:
        raise ValueError("No scenes found in JSON")

    srt_blocks = []
    subtitle_index = 1
    current_time = 0.0

    for scene in scenes:
        duration = scene.get("audio_duration", 0)
        if duration <= 0:
            continue

        text = (
            scene.get("narration") or
            scene.get("description") or
            scene.get("text") or
            ""
        ).strip()

        if not text:
            current_time += duration
            continue

        phrases = split_into_phrases(text)

        if not phrases:
            current_time += duration
            continue

        phrase_duration = duration / len(phrases)

        for phrase in phrases:
            start = current_time
            end = start + phrase_duration

            srt_blocks.append(str(subtitle_index))
            srt_blocks.append(
                f"{format_srt_time(start)} --> {format_srt_time(end)}"
            )
            srt_blocks.append(phrase)
            srt_blocks.append("")

            subtitle_index += 1
            current_time = end

    with open(output_srt, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(srt_blocks))

    print(f" Phrase-by-phrase subtitles generated → {output_srt}")
    print(f" Total subtitle entries: {subtitle_index - 1}")


def validate_srt_file(srt_file: str):
    with open(srt_file, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    if not lines[0].isdigit():
        print(" Invalid SRT: Missing index")
        return False

    if "-->" not in lines[1]:
        print(" Invalid SRT: Missing timestamp")
        return False

    print(" SRT format validated successfully")
    return True


if __name__ == "__main__":
    generate_srt_from_scenes(
        input_json="output/scenes_with_audio.json",
        output_srt="output/subtitles2.srt"
    )

    validate_srt_file("output/subtitles2.srt")
