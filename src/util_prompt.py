# src/util_prompt.py

def validate_scene(scene):
    required_keys = {
        "scene_id": int,
        "description": str,
        "visual_focus": str
    }

    for key, expected_type in required_keys.items():
        if key not in scene:
            raise ValueError(f"Missing required scene field: {key}")
        if not isinstance(scene[key], expected_type):
            raise TypeError(f"{key} must be {expected_type}")
