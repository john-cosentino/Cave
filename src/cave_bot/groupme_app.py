#!/usr/bin/env python3

import os
import requests
from flask import Flask, request, jsonify

from cave_bot.ai_reply import generate_persona_reply, get_model, is_ai_enabled
from cave_bot.authorization import get_admin_ids_from_env, is_admin
from cave_bot.persona_registry import PersonaRegistry
from cave_bot.personas import PersonaError

app = Flask(__name__)

GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")
BOT_TRIGGER = os.getenv("BOT_TRIGGER", "cavebot").lower()
PERSONA_REGISTRY = PersonaRegistry.from_profiles_dir()
ADMIN_IDS = get_admin_ids_from_env()
AI_ENABLED = is_ai_enabled()
AI_MODEL = get_model()

_anthropic_client = None


def get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic

        _anthropic_client = anthropic.Anthropic()
    return _anthropic_client


def send_groupme_message(text: str) -> None:
    if not GROUPME_BOT_ID:
        print("GROUPME_BOT_ID is not set. Cannot send message.")
        return

    response = requests.post(
        "https://api.groupme.com/v3/bots/post",
        params={
            "bot_id": GROUPME_BOT_ID,
            "text": text,
        },
        timeout=10,
    )

    print(f"GroupMe post status: {response.status_code}")
    if response.text:
        print(response.text)


def match_persona_alias(text: str, registry: PersonaRegistry):
    """If text starts with '<alias>:', return (persona, remainder); else None."""
    if ":" not in text:
        return None

    prefix, _, remainder = text.partition(":")
    persona = registry.find_by_alias(prefix)

    if persona is None:
        return None

    return persona, remainder.strip()


def parse_character_command(lowered_text: str):
    """Return ('list', None), ('status', None), ('switch', key), or None."""
    if "characters" in lowered_text:
        return "list", None

    if "character" not in lowered_text:
        return None

    after = lowered_text[lowered_text.find("character") + len("character"):].strip()

    if not after:
        return "status", None

    return "switch", after.split()[0]


def format_character_list(registry: PersonaRegistry) -> str:
    names = ", ".join(f"{p['display_name']} ({p['key']})" for p in registry.list_personas())
    return f"Available characters: {names}"


def build_reply(
    sender_name: str,
    message_text: str,
    registry: PersonaRegistry,
    sender_id: str | None = None,
    admin_ids: frozenset[str] = frozenset(),
    ai_enabled: bool = False,
    ai_client: object | None = None,
    ai_model: str = AI_MODEL,
) -> str | None:
    text = (message_text or "").strip()

    persona_match = match_persona_alias(text, registry)
    if persona_match:
        persona, question = persona_match

        if ai_enabled and question and ai_client is not None:
            try:
                answer = generate_persona_reply(ai_client, persona, question, model=ai_model)
                return f"[{persona['display_name']}] {answer}"
            except Exception as exc:
                print(f"AI reply failed for persona '{persona['key']}': {exc}")

        greeting = persona.get("greeting") or f"{persona['display_name']} is listening."
        suffix = "" if ai_enabled else " (I can't answer questions yet.)"
        return f"[{persona['display_name']}] {greeting}{suffix}"

    lowered = text.lower()

    if BOT_TRIGGER not in lowered:
        return None

    character_command = parse_character_command(lowered)
    if character_command is not None:
        action, key = character_command

        if action == "list":
            return format_character_list(registry)

        if action == "status":
            active = registry.get_active()
            return f"Current character: {active['display_name']} ({active['key']})"

        if not is_admin(sender_id, admin_ids):
            return "Sorry, only a Cave Bot admin can change characters."

        try:
            persona = registry.set_active(key)
        except PersonaError:
            return f"Unknown character '{key}'. Try: cavebot characters"

        return f"Character switched to {persona['display_name']}."

    if "help" in lowered:
        return (
            "Cave Bot commands: "
            "cavebot help, cavebot ping, cavebot status, cavebot vibe, cavebot rules, "
            "cavebot characters, cavebot character, cavebot character <key>"
        )

    if "ping" in lowered:
        return "pong"

    if "vibe" in lowered:
        return "The Cave is operational. Morale is questionable but stable."

    if "status" in lowered:
        return "Cave Bot status: online. Webhook is running. GroupMe posting works."

    if "rules" in lowered:
        return "Cave rules: be funny, don't be a jerk, and don't make the bot sentient before lunch."

#    if "vibe" in lowered:
#        return "The Cave is operational. Morale is questionable but stable."
#
#    if "rules" in lowered:
#        return "Cave rules: be funny, don't be a jerk, and don't make the bot sentient before lunch."

    return f"Hey {sender_name}, Cave Bot heard you. Try: cavebot help"


@app.get("/")
def health_check():
    return jsonify({"status": "ok", "service": "cave-bot"})


@app.post("/groupme/callback")
def groupme_callback():
    payload = request.get_json(silent=True) or {}
    print("Incoming GroupMe payload:", payload)

    sender_type = payload.get("sender_type")
    sender_name = payload.get("name", "there")
    sender_id = payload.get("user_id")
    text = payload.get("text", "")

    # Avoid responding to bot messages, including our own.
    if sender_type == "bot":
        return jsonify({"status": "ignored bot message"}), 200

    reply = build_reply(
        sender_name,
        text,
        PERSONA_REGISTRY,
        sender_id=sender_id,
        admin_ids=ADMIN_IDS,
        ai_enabled=AI_ENABLED,
        ai_client=get_anthropic_client() if AI_ENABLED else None,
        ai_model=AI_MODEL,
    )

    if reply:
        send_groupme_message(reply)
        return jsonify({"status": "replied"}), 200

    return jsonify({"status": "ignored"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
