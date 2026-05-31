<p align="center">
  <img src="assets/mind-your-skill-logo.png" alt="Mind Your Skill — open-source skill library for Hermes Agent" width="100%" />
</p>

<p align="center">
  <strong>Open-source skill library for Hermes Agent.</strong><br />
  Modular skills that teach agents how to work — not just how to reply.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-0f172a.svg"></a>
  <img alt="Status" src="https://img.shields.io/badge/status-beta-2563eb.svg">
  <img alt="Hermes Agent" src="https://img.shields.io/badge/Hermes-Agent-7c3aed.svg">
  <img alt="Skill Library" src="https://img.shields.io/badge/skill%20library-modular-06b6d4.svg">
</p>

---

## What is Mind Your Skill?

**Mind Your Skill** is a curated open-source skill library for **Hermes Agent**.

The goal is simple: make agents more useful, consistent, and reusable through modular skill packages. Each skill has a clear entrypoint, focused references, setup flow, runtime behavior, examples, and security notes.

This repository is designed for skills that feel production-minded: easy to inspect, easy to extend, and practical for real workflows.

## Available Skills

### MoneyClip

**MoneyClip** is a personal expense tracking skill for Indonesian daily chat patterns.

It helps users:

- set starting cash balance
- record daily spending
- infer expense categories
- parse Indonesian amount shorthand like `rb`, `k`, and `jt`
- prepare Google Sheet storage during first setup
- show remaining balance after each transaction
- support recap, edit, and delete flows

Entrypoint:

```text
skills/moneyclip/SKILL.md
```

Documentation:

```text
skills/moneyclip/README.md
```

## Skill Creator Prompt

Use the reusable prompt below when you have a new idea and want an AI assistant to turn it into a professional Hermes Agent skill package:

```text
prompts/professional-hermes-skill-creator.md
```

## MoneyClip in action

```text
User: pakai moneyclip
Agent: Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.

User: makan 25rb
Agent: ✅ makan Rp25.000
       💰 Sisa: Rp175.000
```

## Repository Structure

```text
Mind-your-skill/
├─ README.md
├─ registry.json
├─ LICENSE
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ CODE_OF_CONDUCT.md
├─ assets/
│  └─ mind-your-skill-logo.png
├─ prompts/
│  └─ professional-hermes-skill-creator.md
└─ skills/
   └─ moneyclip/
      ├─ SKILL.md
      ├─ README.md
      └─ references/
         ├─ setup.md
         ├─ runtime.md
         ├─ sheets-schema.md
         └─ examples.md
```

## Skill Philosophy

Skills should help agents work consistently, not just respond creatively.

A good skill should be:

- **modular** — separate setup, runtime, examples, and references
- **auditable** — clear instructions and explicit permissions
- **safe by default** — no hidden endpoint or destructive behavior
- **token-aware** — load only the smallest relevant reference
- **beginner-friendly** — guide first-time users without manual docs overload
- **repeatable** — behave reliably across daily use

## Hermes-style Progressive Loading

Mind Your Skill follows a modular pattern designed for Hermes Agent:

- `SKILL.md` is the entrypoint and router.
- `references/setup.md` is loaded only during first-run setup.
- `references/runtime.md` is loaded for daily use.
- `references/sheets-schema.md` is loaded only when preparing Google Sheets.
- `references/examples.md` is loaded only when examples are needed.

This keeps common workflows lighter and easier to maintain.

## Security

Skills may guide agents to edit files, write to spreadsheets, or call configured endpoints. For that reason, every skill should be explicit about permissions and safe behavior.

See `SECURITY.md` for the project security policy.

## Contributing

Contributions are welcome.

Before adding or changing skills, read:

```text
CONTRIBUTING.md
```

New skills should follow the modular structure and be added to `registry.json`.

## License

This project is licensed under the MIT License.
