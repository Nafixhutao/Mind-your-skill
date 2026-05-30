# Mind Your Skill

**Mind Your Skill** is an open-source skill library for Hermes Agent.

This repository is designed as a curated collection of modular agent skills: each skill has a clear entrypoint, setup flow, runtime behavior, examples, and security notes.

## Philosophy

Skills should help agents work consistently, not just reply creatively.

A good skill should be:

- Modular
- Easy to audit
- Safe by default
- Token-aware
- Clear for first-time users
- Reliable during repeated runtime use

## Repository structure

```text
Mind-your-skill/
├─ README.md
├─ registry.json
├─ LICENSE
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ CODE_OF_CONDUCT.md
└─ skills/
   └─ moneyclip/
      ├─ SKILL.md
      ├─ README.md
      ├─ setup.md
      ├─ runtime.md
      ├─ sheets-schema.md
      └─ examples.md
```

## Available skills

### MoneyClip

MoneyClip is a personal expense tracking skill for Indonesian daily chat patterns.

It can:

- Guide first-time setup with a Google Sheet link
- Prepare required Google Sheet tabs and headers
- Set starting cash balance
- Record daily spending
- Infer expense categories
- Handle Indonesian amount shorthand like `rb`, `k`, and `jt`
- Show remaining balance
- Support recap, edit, and delete flows

Skill entrypoint:

```text
skills/moneyclip/SKILL.md
```

Skill documentation:

```text
skills/moneyclip/README.md
```

## MoneyClip example

User:

```text
pakai moneyclip
```

Agent:

```text
Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.
```

User:

```text
makan 25rb
```

Agent:

```text
✅ makan Rp25.000
💰 Sisa: Rp175.000
```

## Skill package model

Each skill should be organized as a package under `skills/<skill-name>/`.

Recommended files:

```text
skills/<skill-name>/
├─ SKILL.md        # entrypoint and router
├─ README.md       # human documentation
├─ setup.md        # first-run setup flow
├─ runtime.md      # compact daily-use behavior
├─ examples.md     # optional examples
└─ changelog.md    # optional version history
```

`SKILL.md` should stay short. Long tutorials, examples, schemas, and implementation details should live in supporting files.

## Token-aware design

Mind Your Skill follows a modular pattern:

- Setup instructions are used only during setup.
- Runtime instructions are compact and used for daily behavior.
- Examples are used only when users ask for help.
- README files are for humans and should not be treated as runtime instructions.

This structure keeps skills easier to maintain and can reduce token usage in agents that support selective skill loading.

## Security

Skills may guide agents to edit files, write to spreadsheets, or call configured endpoints. For that reason, every skill should be auditable and explicit about permissions.

See `SECURITY.md` for the project security policy.

## Contributing

Contributions are welcome.

Before adding a skill, read:

```text
CONTRIBUTING.md
```

New skills should follow the modular structure and be added to `registry.json`.

## License

This project is licensed under the MIT License.
