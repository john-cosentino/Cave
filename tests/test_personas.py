#!/usr/bin/env python3

import json
import tempfile
import unittest
from pathlib import Path

from cave_bot.personas import (
    DEFAULT_PROFILES_DIR,
    PersonaError,
    load_personas,
    validate_persona,
)


class ValidatePersonaTests(unittest.TestCase):
    def test_valid_persona_passes(self):
        validate_persona(
            {
                "key": "santa",
                "display_name": "Santa Claus",
                "aliases": ["santa", "santa claus"],
                "system_prompt": "You are Santa Claus.",
            }
        )

    def test_missing_field_raises(self):
        with self.assertRaises(PersonaError):
            validate_persona({"key": "santa"})

    def test_non_lowercase_key_raises(self):
        with self.assertRaises(PersonaError):
            validate_persona(
                {
                    "key": "Santa",
                    "display_name": "Santa Claus",
                    "aliases": ["santa"],
                    "system_prompt": "You are Santa Claus.",
                }
            )

    def test_empty_aliases_raises(self):
        with self.assertRaises(PersonaError):
            validate_persona(
                {
                    "key": "santa",
                    "display_name": "Santa Claus",
                    "aliases": [],
                    "system_prompt": "You are Santa Claus.",
                }
            )

    def test_non_string_type_raises(self):
        with self.assertRaises(PersonaError):
            validate_persona([])


class LoadPersonasTests(unittest.TestCase):
    def test_loads_valid_persona_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            profiles_dir = Path(tmp)
            (profiles_dir / "santa.json").write_text(
                json.dumps(
                    {
                        "key": "santa",
                        "display_name": "Santa Claus",
                        "aliases": ["santa"],
                        "system_prompt": "You are Santa Claus.",
                    }
                ),
                encoding="utf-8",
            )

            personas = load_personas(profiles_dir)

        self.assertIn("santa", personas)
        self.assertEqual(personas["santa"]["display_name"], "Santa Claus")

    def test_invalid_persona_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            profiles_dir = Path(tmp)
            (profiles_dir / "broken.json").write_text(
                json.dumps({"key": "broken"}), encoding="utf-8"
            )

            with self.assertRaises(PersonaError):
                load_personas(profiles_dir)

    def test_duplicate_key_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            profiles_dir = Path(tmp)
            persona = {
                "key": "santa",
                "display_name": "Santa Claus",
                "aliases": ["santa"],
                "system_prompt": "You are Santa Claus.",
            }
            (profiles_dir / "a.json").write_text(json.dumps(persona), encoding="utf-8")
            (profiles_dir / "b.json").write_text(json.dumps(persona), encoding="utf-8")

            with self.assertRaises(PersonaError):
                load_personas(profiles_dir)

    def test_missing_directory_returns_empty(self):
        personas = load_personas(Path("/nonexistent/path/for/cave-bot-tests"))
        self.assertEqual(personas, {})


class RepoPersonaProfilesTests(unittest.TestCase):
    def test_default_profiles_dir_loads_cleanly(self):
        personas = load_personas(DEFAULT_PROFILES_DIR)
        self.assertIn("cavebot", personas)
        self.assertIn("system_prompt", personas["cavebot"])

    def test_seasonal_personas_are_present(self):
        personas = load_personas(DEFAULT_PROFILES_DIR)
        self.assertIn("santa", personas)
        self.assertIn("easter_bunny", personas)


if __name__ == "__main__":
    unittest.main()
