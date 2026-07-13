#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_PROFILES_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "personas" / "profiles"

REQUIRED_FIELDS = {"key", "display_name", "aliases", "system_prompt"}


class PersonaError(ValueError):
    """Raised when a persona definition is missing or invalid."""


def validate_persona(data: dict[str, Any], source: str = "<unknown>") -> None:
    if not isinstance(data, dict):
        raise PersonaError(f"{source}: persona definition must be a JSON object")

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise PersonaError(f"{source}: missing required field(s): {', '.join(sorted(missing))}")

    if not isinstance(data["key"], str) or not data["key"].strip():
        raise PersonaError(f"{source}: 'key' must be a non-empty string")

    if data["key"] != data["key"].lower():
        raise PersonaError(f"{source}: 'key' must be lowercase")

    if not isinstance(data["display_name"], str) or not data["display_name"].strip():
        raise PersonaError(f"{source}: 'display_name' must be a non-empty string")

    if not isinstance(data["aliases"], list) or not data["aliases"]:
        raise PersonaError(f"{source}: 'aliases' must be a non-empty list")

    if not all(isinstance(alias, str) and alias.strip() for alias in data["aliases"]):
        raise PersonaError(f"{source}: all 'aliases' entries must be non-empty strings")

    if not isinstance(data["system_prompt"], str) or not data["system_prompt"].strip():
        raise PersonaError(f"{source}: 'system_prompt' must be a non-empty string")


def load_persona_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    validate_persona(data, source=path.name)
    return data


def load_personas(profiles_dir: Path = DEFAULT_PROFILES_DIR) -> dict[str, dict[str, Any]]:
    """Load and validate all persona JSON files in profiles_dir, keyed by persona 'key'."""
    personas: dict[str, dict[str, Any]] = {}

    if not profiles_dir.is_dir():
        return personas

    for path in sorted(profiles_dir.glob("*.json")):
        persona = load_persona_file(path)
        key = persona["key"]

        if key in personas:
            raise PersonaError(f"duplicate persona key '{key}' in {path.name}")

        personas[key] = persona

    return personas
