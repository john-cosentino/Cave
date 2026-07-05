#!/usr/bin/env python3

import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")
BOT_TRIGGER = os.getenv("BOT_TRIGGER", "cavebot").lower()


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


def build_reply(sender_name: str, message_text: str) -> str | None:
    text = (message_text or "").strip()
    lowered = text.lower()

    if BOT_TRIGGER not in lowered:
        return None

    if "help" in lowered:
        return (
            "Cave Bot commands: "
            "cavebot help, cavebot ping, cavebot status, cavebot vibe, cavebot rules"
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
    text = payload.get("text", "")

    # Avoid responding to bot messages, including our own.
    if sender_type == "bot":
        return jsonify({"status": "ignored bot message"}), 200

    reply = build_reply(sender_name, text)

    if reply:
        send_groupme_message(reply)
        return jsonify({"status": "replied"}), 200

    return jsonify({"status": "ignored"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
