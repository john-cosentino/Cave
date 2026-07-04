# Cave Bot Project Direction

## Purpose

Cave Bot is a personal chatbot project intended to become a useful assistant or interactive tool for friends.

The current goal is not to build the final bot immediately. The current goal is to build the foundation:

- clean GitHub repo structure
- safe public-repo habits
- local Python project
- repeatable development environment
- readable code
- basic tests
- future room for AI/API integration

## Current Version

The current version is a local command-line chatbot.

It does not use an external AI API yet.

## Design Rules

- Do not commit secrets, tokens, passwords, or API keys.
- Do not commit private personal data.
- Keep configuration separate from code.
- Use environment variables for secrets later.
- Keep the code simple and readable.
- Add features one small step at a time.

## Near-Term Roadmap

1. Create local command-line chatbot skeleton.
2. Add basic tests.
3. Add logging.
4. Add configuration file support.
5. Add conversation history storage.
6. Add a safer plugin/tool structure.
7. Add external AI integration later.
8. Add web or chat interface later.
