---
name: mind-your-skill
description: Open-source Hermes Agent skill library router. Use this file to discover and load skills from this repository.
version: 0.1.0
metadata:
  hermes:
    category: skill-library
    tags:
      - hermes
      - skills
      - skill-library
      - open-source
    registry: registry.json
---

# Mind Your Skill Router

Use this file when a user gives the repository URL and asks Hermes Agent to load available skills.

Repository:

```text
https://github.com/Nafixhutao/Mind-your-skill
```

Registry:

```text
registry.json
```

Raw registry URL:

```text
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/registry.json
```

## How to load skills

1. Read `registry.json`.
2. Show the available skills to the user.
3. Ask which skill to activate, unless the user already named one.
4. Load that skill's `SKILL.md` entrypoint.
5. Follow the selected skill's setup/runtime instructions.

If there is only one skill in the registry and the user did not specify a skill, offer to activate it.

## Available skill

### personal-finance-ledger

Tracks personal income and expenses from free text or receipt images, then saves records to Google Sheets.

Entrypoint:

```text
skills/personal-finance-ledger/SKILL.md
```

Raw entrypoint URL:

```text
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/skills/personal-finance-ledger/SKILL.md
```

## Fallback behavior

If GitHub search cannot find this repository, do not search again. Use the direct URL or raw URLs above.

If the runtime cannot fetch GitHub content automatically, ask the user to paste the raw `SKILL.md` content or clone the repository manually.
