#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import Any, Mapping

AI_ENABLED_ENV_VAR = "CAVE_BOT_AI_ENABLED"
MODEL_ENV_VAR = "CAVE_BOT_MODEL"
DEFAULT_MODEL = "claude-opus-4-8"
MAX_TOKENS = 512

TRUTHY_VALUES = {"1", "true", "yes", "on"}


def is_ai_enabled(env: Mapping[str, str] = os.environ) -> bool:
    return env.get(AI_ENABLED_ENV_VAR, "").strip().lower() in TRUTHY_VALUES


def get_model(env: Mapping[str, str] = os.environ) -> str:
    return env.get(MODEL_ENV_VAR) or DEFAULT_MODEL


def generate_persona_reply(
    client: Any,
    persona: dict[str, Any],
    question: str,
    model: str = DEFAULT_MODEL,
) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=persona["system_prompt"],
        messages=[{"role": "user", "content": question}],
    )
    return next(block.text for block in response.content if block.type == "text")
