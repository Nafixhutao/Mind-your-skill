# Mind Your Skill Quickstart

This repository is an open-source Hermes Agent skill library.

Repository URL:

```text
https://github.com/Nafixhutao/Mind-your-skill
```

Raw registry URL:

```text
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/registry.json
```

Root router:

```text
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/SKILL.md
```

## For Hermes Agent users

Send this to Hermes:

```text
Load this Hermes skill library:
https://github.com/Nafixhutao/Mind-your-skill

If repository search fails, use this raw registry:
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/registry.json

Show available skills, then ask which one I want to activate.
```

## Activate Personal Finance Ledger directly

Send this to Hermes:

```text
Load the Hermes skill personal-finance-ledger from:
https://github.com/Nafixhutao/Mind-your-skill

If search fails, use this direct raw SKILL.md URL:
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/skills/personal-finance-ledger/SKILL.md

Then follow its setup/runtime instructions.
```

## Available skills

### personal-finance-ledger

Personal income and expense tracker.

Capabilities:

- record expenses from text, such as `beli kopi 15rb`
- record income, such as `gajian 5jt`
- read receipt images when OCR is available
- save transactions to Google Sheets
- show monthly balance and category summaries

Entrypoint:

```text
skills/personal-finance-ledger/SKILL.md
```

Raw entrypoint:

```text
https://raw.githubusercontent.com/Nafixhutao/Mind-your-skill/main/skills/personal-finance-ledger/SKILL.md
```

## Required setup for personal-finance-ledger

The runtime must provide:

```text
GOOGLE_SERVICE_ACCOUNT_JSON
FINANCE_SHEET_ID
```

Optional:

```text
FINANCE_TRANSACTIONS_SHEET_NAME=Transactions
FINANCE_DEFAULT_CURRENCY=IDR
FINANCE_DEFAULT_TIMEZONE=Asia/Jakarta
```

The Google Sheet must be shared with the service account email as Editor.

## Troubleshooting

If Hermes says it cannot find the repo:

1. Use the raw registry URL.
2. Use the raw SKILL.md URL.
3. Clone manually:

```bash
git clone https://github.com/Nafixhutao/Mind-your-skill.git
```

Then point Hermes to:

```text
Mind-your-skill/SKILL.md
```
