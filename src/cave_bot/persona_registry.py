#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Any

from cave_bot.personas import DEFAULT_PROFILES_DIR, PersonaError, load_personas


class PersonaRegistry:
    """Holds loaded personas plus which one is currently active.

    This is an in-memory registry: active-persona state lives only for the
    lifetime of the instance and is not persisted across process restarts.
    """

    def __init__(self, personas: dict[str, dict[str, Any]], default_key: str):
        if default_key not in personas:
            raise PersonaError(f"default persona key '{default_key}' not found among loaded personas")

        self._personas = personas
        self._default_key = default_key
        self._active_key = default_key

    @classmethod
    def from_profiles_dir(
        cls,
        profiles_dir: Path = DEFAULT_PROFILES_DIR,
        default_key: str = "cavebot",
    ) -> "PersonaRegistry":
        personas = load_personas(profiles_dir)
        return cls(personas, default_key)

    def list_personas(self) -> list[dict[str, Any]]:
        return [self._personas[key] for key in sorted(self._personas)]

    def get_active_key(self) -> str:
        return self._active_key

    def get_active(self) -> dict[str, Any]:
        return self._personas[self._active_key]

    def set_active(self, key: str) -> dict[str, Any]:
        if key not in self._personas:
            raise PersonaError(f"unknown persona key '{key}'")

        self._active_key = key
        return self._personas[key]

    def reset_to_default(self) -> dict[str, Any]:
        self._active_key = self._default_key
        return self._personas[self._default_key]

    def find_by_alias(self, text: str) -> dict[str, Any] | None:
        """Return the persona whose alias list contains text (case-insensitive), or None."""
        lowered = text.strip().lower()

        for persona in self._personas.values():
            if lowered in (alias.lower() for alias in persona["aliases"]):
                return persona

        return None
