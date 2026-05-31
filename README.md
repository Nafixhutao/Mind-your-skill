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

## How to use this repository

Give Hermes Agent this repository URL:

```text
https://github.com/Nafixhutao/Mind-your-skill
```

Then ask Hermes to read:

```text
registry.json
```

The registry tells Hermes which skills are available and where each skill entrypoint is located.

A typical skill entrypoint looks like this:

```text
skills/<skill-name>/SKILL.md
```

`SKILL.md` is the router. It tells Hermes when the skill should activate and which reference file to read for setup, runtime, schema, or examples.

## Prompt for Hermes

```text
Load skills from this GitHub repository:
https://github.com/Nafixhutao/Mind-your-skill

Read registry.json, show the available skills, then ask me which skill I want to activate.
After I choose one, load its SKILL.md entrypoint and follow the setup/runtime instructions.
```

If you already know the skill name:

```text
Load the skill personal-finance-ledger from this GitHub repository:
https://github.com/Nafixhutao/Mind-your-skill

Read registry.json, then load:
skills/personal-finance-ledger/SKILL.md
```

## Available Skills

### Personal Finance Ledger

A personal income and expense tracking skill.

It can help users:

- record expenses from free text, such as `beli kopi 15rb`
- record income, such as `gajian 5jt`
- read receipt images when OCR is available
- infer categories automatically
- save transactions to Google Sheets
- summarize balance, income, expenses, and category totals

Entrypoint:

```text
skills/personal-finance-ledger/SKILL.md
```

Documentation:

```text
skills/personal-finance-ledger/README.md
```

Main requirements:

- Google Sheets access
- service account credential configured securely in the runtime
- target Google Sheet ID
- optional OCR/file input support for receipt images

## Example usage

```text
User: beli kopi 15rb
Agent: Tercatat: pengeluaran Rp15.000 untuk Makanan & Minuman.

User: gajian 5jt
Agent: Tercatat: pemasukan Rp5.000.000 untuk Gaji.

User: ringkasan bulan ini
Agent: Ringkasan bulan ini:
Saldo: Rp4.250.000
Pemasukan: Rp7.000.000
Pengeluaran: Rp2.750.000
Kategori terbesar: Makanan & Minuman — Rp850.000
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
├─ prompts/
└─ skills/
   └─ personal-finance-ledger/
      ├─ SKILL.md
      ├─ README.md
      └─ references/
         ├─ setup.md
         ├─ runtime.md
         ├─ schema.md
         └─ examples.md
```

## Skill Philosophy

A good Hermes skill should be:

- modular
- auditable
- safe by default
- token-aware
- beginner-friendly
- repeatable

## Hermes-style Progressive Loading

- `registry.json` lists available skills.
- `SKILL.md` is the entrypoint and router.
- `references/setup.md` is loaded only during setup or troubleshooting.
- `references/runtime.md` is loaded for daily use.
- `references/schema.md` is loaded only when structured data is needed.
- `references/examples.md` is loaded only when examples are needed.

## Security

Do not hardcode secrets in skill files. Use environment variables or the runtime secret manager.

See `SECURITY.md` for the project security policy.

## Contributing

Contributions are welcome. New skills should follow the modular structure and be added to `registry.json`.

## License

This project is licensed under the MIT License.
