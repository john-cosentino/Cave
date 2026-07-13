#!/usr/bin/env python3

import unittest

from cave_bot.persona_registry import PersonaRegistry
from cave_bot.personas import DEFAULT_PROFILES_DIR, PersonaError

CAVEBOT = {
    "key": "cavebot",
    "display_name": "Cave Bot",
    "aliases": ["cavebot"],
    "system_prompt": "You are Cave Bot.",
}

SANTA = {
    "key": "santa",
    "display_name": "Santa Claus",
    "aliases": ["santa", "santa claus"],
    "system_prompt": "You are Santa Claus.",
}


def make_registry() -> PersonaRegistry:
    return PersonaRegistry({"cavebot": CAVEBOT, "santa": SANTA}, default_key="cavebot")


class PersonaRegistryInitTests(unittest.TestCase):
    def test_unknown_default_key_raises(self):
        with self.assertRaises(PersonaError):
            PersonaRegistry({"cavebot": CAVEBOT}, default_key="santa")

    def test_active_persona_starts_as_default(self):
        registry = make_registry()
        self.assertEqual(registry.get_active_key(), "cavebot")
        self.assertEqual(registry.get_active(), CAVEBOT)


class PersonaRegistryListTests(unittest.TestCase):
    def test_list_personas_is_sorted_by_key(self):
        registry = make_registry()
        keys = [p["key"] for p in registry.list_personas()]
        self.assertEqual(keys, ["cavebot", "santa"])


class PersonaRegistrySetActiveTests(unittest.TestCase):
    def test_set_active_switches_persona(self):
        registry = make_registry()
        result = registry.set_active("santa")

        self.assertEqual(result, SANTA)
        self.assertEqual(registry.get_active_key(), "santa")
        self.assertEqual(registry.get_active(), SANTA)

    def test_set_active_unknown_key_raises_and_leaves_state_unchanged(self):
        registry = make_registry()

        with self.assertRaises(PersonaError):
            registry.set_active("easter_bunny")

        self.assertEqual(registry.get_active_key(), "cavebot")

    def test_reset_to_default_restores_default_after_switch(self):
        registry = make_registry()
        registry.set_active("santa")

        result = registry.reset_to_default()

        self.assertEqual(result, CAVEBOT)
        self.assertEqual(registry.get_active_key(), "cavebot")


class PersonaRegistryFindByAliasTests(unittest.TestCase):
    def test_find_by_alias_matches_case_insensitively(self):
        registry = make_registry()
        self.assertEqual(registry.find_by_alias("SANTA"), SANTA)
        self.assertEqual(registry.find_by_alias("Santa Claus"), SANTA)

    def test_find_by_alias_no_match_returns_none(self):
        registry = make_registry()
        self.assertIsNone(registry.find_by_alias("easter bunny"))


class PersonaRegistryFromProfilesDirTests(unittest.TestCase):
    def test_loads_real_profiles_dir_with_cavebot_default(self):
        registry = PersonaRegistry.from_profiles_dir(DEFAULT_PROFILES_DIR, default_key="cavebot")
        self.assertEqual(registry.get_active_key(), "cavebot")
        self.assertIn("cavebot", [p["key"] for p in registry.list_personas()])


if __name__ == "__main__":
    unittest.main()
