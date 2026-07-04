#!/usr/bin/env python3

"""
Cave Bot

A simple local chatbot skeleton.

This version does not use an external AI API yet.
It is meant to establish project structure, command-line interaction,
logging habits, and safe configuration practices.
"""

from datetime import datetime


def get_response(user_input: str) -> str:
    """
    Return a simple response based on user input.

    This is intentionally basic for now. Later, this function can be replaced
    or expanded to call a real language model, search notes, read files,
    or use a more advanced decision system.
    """
    cleaned = user_input.strip().lower()

    if cleaned in {"quit", "exit", "q"}:
        return "EXIT"

    if "hello" in cleaned or "hi" in cleaned:
        return "Hey. Cave Bot is online."

    if "time" in cleaned:
        return f"The current system time is {datetime.now()}."

    if "help" in cleaned:
        return (
            "Try asking me something simple. "
            "For now I understand: hello, time, help, quit."
        )

    return "I heard you, but I do not know how to respond to that yet."


def main() -> None:
    print("Cave Bot started.")
    print("Type 'help' for options. Type 'quit' to exit.")
    print()

    while True:
        user_input = input("You: ")
        response = get_response(user_input)

        if response == "EXIT":
            print("Cave Bot: Later.")
            break

        print(f"Cave Bot: {response}")


if __name__ == "__main__":
    main()
