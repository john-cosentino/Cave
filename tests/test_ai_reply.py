#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from cave_bot.ai_reply import (
    AI_ENABLED_ENV_VAR,
    DEFAULT_MODEL,
    MODEL_ENV_VAR,
    generate_persona_reply,
    get_model,
    is_ai_enabled,
)

PERSONA = {
    "key": "santa",
    "display_name": "Santa Claus",
    "aliases": ["santa"],
    "system_prompt": "You are Santa Claus.",
}


class IsAiEnabledTests(unittest.TestCase):
    def test_missing_env_defaults_false(self):
        self.assertFalse(is_ai_enabled({}))

    def test_true_values(self):
        for value in ["1", "true", "True", "YES", "on"]:
            self.assertTrue(is_ai_enabled({AI_ENABLED_ENV_VAR: value}), value)

    def test_false_values(self):
        for value in ["0", "false", "no", "", "off", "garbage"]:
            self.assertFalse(is_ai_enabled({AI_ENABLED_ENV_VAR: value}), value)


class GetModelTests(unittest.TestCase):
    def test_default_model_when_unset(self):
        self.assertEqual(get_model({}), DEFAULT_MODEL)

    def test_custom_model_from_env(self):
        self.assertEqual(get_model({MODEL_ENV_VAR: "claude-haiku-4-5"}), "claude-haiku-4-5")


def make_fake_client(response_text: str):
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = response_text

    response = MagicMock()
    response.content = [text_block]

    client = MagicMock()
    client.messages.create.return_value = response
    return client


class GeneratePersonaReplyTests(unittest.TestCase):
    def test_returns_text_from_response(self):
        client = make_fake_client("Ho ho ho!")
        result = generate_persona_reply(client, PERSONA, "What should I get for Christmas?")
        self.assertEqual(result, "Ho ho ho!")

    def test_passes_persona_system_prompt_and_question(self):
        client = make_fake_client("Ho ho ho!")
        generate_persona_reply(client, PERSONA, "Gifts?", model="claude-haiku-4-5")

        _, kwargs = client.messages.create.call_args
        self.assertEqual(kwargs["system"], PERSONA["system_prompt"])
        self.assertEqual(kwargs["messages"], [{"role": "user", "content": "Gifts?"}])
        self.assertEqual(kwargs["model"], "claude-haiku-4-5")

    def test_ignores_non_text_blocks(self):
        other_block = MagicMock()
        other_block.type = "thinking"

        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = "Final answer"

        response = MagicMock()
        response.content = [other_block, text_block]

        client = MagicMock()
        client.messages.create.return_value = response

        result = generate_persona_reply(client, PERSONA, "Q?")
        self.assertEqual(result, "Final answer")


if __name__ == "__main__":
    unittest.main()
