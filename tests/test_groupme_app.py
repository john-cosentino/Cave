#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from cave_bot.groupme_app import PERSONA_REGISTRY, build_reply, match_persona_alias
from cave_bot.persona_registry import PersonaRegistry

WIZARD = {
    "key": "wizard",
    "display_name": "Wizard",
    "aliases": ["wizard"],
    "system_prompt": "You are a Wizard.",
    "greeting": "The Wizard appears in a puff of smoke.",
}


def make_wizard_registry() -> PersonaRegistry:
    return PersonaRegistry({"wizard": WIZARD}, default_key="wizard")


CAVEBOT = {
    "key": "cavebot",
    "display_name": "Cave Bot",
    "aliases": ["cavebot"],
    "system_prompt": "You are Cave Bot.",
}

SANTA = {
    "key": "santa",
    "display_name": "Santa Claus",
    "aliases": ["santa"],
    "system_prompt": "You are Santa Claus.",
}


def make_multi_persona_registry() -> PersonaRegistry:
    return PersonaRegistry({"cavebot": CAVEBOT, "santa": SANTA}, default_key="cavebot")


class MatchPersonaAliasTests(unittest.TestCase):
    def test_matches_known_alias_prefix(self):
        result = match_persona_alias("cavebot: are you there?", PERSONA_REGISTRY)
        self.assertIsNotNone(result)
        persona, remainder = result
        self.assertEqual(persona["key"], "cavebot")
        self.assertEqual(remainder, "are you there?")

    def test_case_insensitive_alias_match(self):
        self.assertIsNotNone(match_persona_alias("CaveBot: hello", PERSONA_REGISTRY))

    def test_unknown_alias_prefix_returns_none(self):
        self.assertIsNone(match_persona_alias("grinch: gifts please", PERSONA_REGISTRY))

    def test_no_colon_returns_none(self):
        self.assertIsNone(match_persona_alias("cavebot help", PERSONA_REGISTRY))


class BuildReplyPersonaRoutingTests(unittest.TestCase):
    def test_persona_prefixed_message_returns_persona_reply(self):
        reply = build_reply("Alice", "cavebot: are you there?", PERSONA_REGISTRY)
        self.assertIn("Cave Bot", reply)

    def test_persona_prefix_bypasses_bot_trigger_word_gate(self):
        registry = make_wizard_registry()
        reply = build_reply("Alice", "wizard: what time is it?", registry)
        self.assertIsNotNone(reply)
        self.assertIn("Wizard", reply)

    def test_unknown_persona_prefix_falls_through_to_normal_gate(self):
        self.assertIsNone(build_reply("Alice", "grinch: gifts please", PERSONA_REGISTRY))


class BuildReplyLegacyCommandTests(unittest.TestCase):
    def test_help_command_still_works(self):
        reply = build_reply("Alice", "cavebot help", PERSONA_REGISTRY)
        self.assertIn("Cave Bot commands", reply)

    def test_ping_command_still_works(self):
        self.assertEqual(build_reply("Alice", "cavebot ping", PERSONA_REGISTRY), "pong")

    def test_untriggered_message_returns_none(self):
        self.assertIsNone(build_reply("Alice", "just chatting", PERSONA_REGISTRY))

    def test_untriggered_message_returns_none_even_without_colon(self):
        registry = make_wizard_registry()
        self.assertIsNone(build_reply("Alice", "hello there", registry))


class BuildReplyCharacterCommandTests(unittest.TestCase):
    def test_characters_lists_all_personas(self):
        registry = make_multi_persona_registry()
        reply = build_reply("Alice", "cavebot characters", registry)
        self.assertIn("Cave Bot", reply)
        self.assertIn("Santa Claus", reply)

    def test_character_with_no_args_shows_active_persona(self):
        registry = make_multi_persona_registry()
        reply = build_reply("Alice", "cavebot character", registry)
        self.assertIn("Cave Bot", reply)

    def test_character_switch_denied_for_non_admin(self):
        registry = make_multi_persona_registry()
        reply = build_reply(
            "Alice",
            "cavebot character santa",
            registry,
            sender_id="999",
            admin_ids=frozenset({"111"}),
        )
        self.assertIn("admin", reply.lower())
        self.assertEqual(registry.get_active_key(), "cavebot")

    def test_character_switch_allowed_for_admin(self):
        registry = make_multi_persona_registry()
        reply = build_reply(
            "Alice",
            "cavebot character santa",
            registry,
            sender_id="111",
            admin_ids=frozenset({"111"}),
        )
        self.assertIn("Santa Claus", reply)
        self.assertEqual(registry.get_active_key(), "santa")

    def test_character_switch_unknown_key_for_admin(self):
        registry = make_multi_persona_registry()
        reply = build_reply(
            "Alice",
            "cavebot character easter_bunny",
            registry,
            sender_id="111",
            admin_ids=frozenset({"111"}),
        )
        self.assertIn("Unknown character", reply)
        self.assertEqual(registry.get_active_key(), "cavebot")

    def test_character_switch_with_no_admin_ids_configured_denies_everyone(self):
        registry = make_multi_persona_registry()
        reply = build_reply("Alice", "cavebot character santa", registry, sender_id="111")
        self.assertIn("admin", reply.lower())
        self.assertEqual(registry.get_active_key(), "cavebot")


class BuildReplyAiRoutingTests(unittest.TestCase):
    def make_client(self, response_text: str) -> MagicMock:
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = response_text

        response = MagicMock()
        response.content = [text_block]

        client = MagicMock()
        client.messages.create.return_value = response
        return client

    def test_ai_enabled_uses_client_response(self):
        client = self.make_client("Ho ho ho, try a telescope!")

        reply = build_reply(
            "Alice",
            "cavebot: what should I get for Christmas?",
            PERSONA_REGISTRY,
            ai_enabled=True,
            ai_client=client,
        )

        self.assertEqual(reply, "[Cave Bot] Ho ho ho, try a telescope!")
        client.messages.create.assert_called_once()

    def test_ai_enabled_falls_back_to_greeting_on_client_error(self):
        client = MagicMock()
        client.messages.create.side_effect = RuntimeError("boom")

        reply = build_reply(
            "Alice",
            "cavebot: are you there?",
            PERSONA_REGISTRY,
            ai_enabled=True,
            ai_client=client,
        )

        self.assertIn("Cave Bot", reply)

    def test_ai_enabled_without_question_skips_client_call(self):
        client = self.make_client("unused")

        reply = build_reply(
            "Alice",
            "cavebot:",
            PERSONA_REGISTRY,
            ai_enabled=True,
            ai_client=client,
        )

        client.messages.create.assert_not_called()
        self.assertIn("Cave Bot", reply)

    def test_ai_disabled_never_calls_client(self):
        client = self.make_client("unused")

        build_reply(
            "Alice",
            "cavebot: are you there?",
            PERSONA_REGISTRY,
            ai_enabled=False,
            ai_client=client,
        )

        client.messages.create.assert_not_called()


if __name__ == "__main__":
    unittest.main()
