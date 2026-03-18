import json

from json_repair import repair_json


def parse_json(text: str) -> dict:
    """Parse JSON with automatic repair for malformed responses (e.g. unescaped chars)."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(repair_json(text))
