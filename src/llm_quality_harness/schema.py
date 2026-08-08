from __future__ import annotations

import json


def required_fields_present(response: str, fields: list[str]) -> bool:
    if not fields:
        return True
    try:
        payload = json.loads(response)
    except json.JSONDecodeError:
        return False
    if not isinstance(payload, dict):
        return False
    return all(field in payload for field in fields)

