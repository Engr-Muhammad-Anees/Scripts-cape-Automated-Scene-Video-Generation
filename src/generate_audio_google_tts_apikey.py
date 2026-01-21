import json
import os
import base64
from io import BytesIO
import requests
from pydub import AudioSegment


API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
TTS_ENDPOINT = "https://texttospeech.googleapis.com/v1/text:synthesize"

LANGUAGE_CODE = "en-US"
VOICE_NAME = "en-US-Neural2-D"
AUDIO_FORMAT = "wav"

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


def synthesize_scene_audio(text: str, output_path: str) -> float:
    """
    Generate TTS audio using Google Cloud API Key
    and return duration in seconds.
    """

    payload = {
        "input": {"text": text},
        "voice": {
            "languageCode": LANGUAGE_CODE,
            "name": VOICE_NAME
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16"
        }
    }

    response = requests.post(
        f"{TTS_ENDPOINT}?key={API_KEY}",
        json=payload
    )
    response.raise_for_status()

    # 1 Decode Base64 audio
    audio_base64 = response.json()["audioContent"]
    audio_raw = base64.b64decode(audio_base64)

    # 2 Load audio correctly
    audio = AudioSegment.from_file(
        BytesIO(audio_raw),
        format="wav"
    )

    #  Save WAV
    audio.export(output_path, format=AUDIO_FORMAT)

    #  Duration in seconds
    duration = round(len(audio) / 1000, 2)
    return duration



def generate_audio_from_scenes(input_json: str, output_json: str) -> None:

    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    scenes = data["Scenes"]

    for scene in scenes:
        scene_id = scene["scene_id"]
        narration = scene["description"]

        output_audio = os.path.join(
            AUDIO_DIR, f"scene_{scene_id:02d}.wav"
        )

        print(f"🎙 Generating audio for Scene {scene_id}")

        duration = synthesize_scene_audio(
            narration,
            output_audio
        )

        scene["audio_file"] = output_audio
        scene["audio_duration"] = duration

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"Scenes": scenes}, f, indent=2)

    print(f"\n Audio generation completed → {output_json}")


if __name__ == "__main__":
    generate_audio_from_scenes(
        input_json="output/scenes_enhanced.json",
        output_json="output/scenes_with_audio.json"
    )
