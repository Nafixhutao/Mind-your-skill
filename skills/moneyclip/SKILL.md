---
name: moneyclip
description: Personal expense tracking skill for Hermes Agent. Uses Google Sheets API helper scripts to create and manage a MoneyClip spreadsheet after one-time Google authorization.
version: 4.7.0
metadata:
  hermes:
    tags: [finance, expense-tracker, telegram, google-sheets, indonesia]
    category: productivity
    mode: auto
    trigger: telegram.message
    requires_toolsets: [terminal]
    config:
      - key: moneyclip.spreadsheet_id
        description: Google Spreadsheet ID created or used by MoneyClip.
        default: ""
        required: false
      - key: moneyclip.spreadsheet_url
        description: Google Spreadsheet URL created or used by MoneyClip.
        default: ""
        required: false
      - key: moneyclip.token_path
        description: Local Google OAuth token path used by MoneyClip helper scripts.
        default: ~/.moneyclip/token.json
        required: false
      - key: moneyclip.timezone
        description: User timezone.
        default: Asia/Jakarta
        required: true
      - key: moneyclip.setup_complete
        description: Whether setup has completed.
        default: "false"
        required: false
---

# MoneyClip

MoneyClip is the official expense tracking skill in this repository.

Use this entrypoint only:

`skills/moneyclip/SKILL.md`

MoneyClip has two phases:

1. **Setup phase** — authorize Google once, create a Google Sheet automatically, prepare tabs, and mark setup as complete.
2. **Runtime phase** — parse balance/spending messages, update the configured spreadsheet through helper scripts, and reply with the remaining balance.

## Tool preference

For Google Sheets operations, use the local helper scripts in `scripts/` when terminal execution is available:

- `scripts/google_auth.py` — authorizes Google Sheets API access and stores a local token.
- `scripts/create_sheet.py` — creates a MoneyClip spreadsheet with required tabs and headers.
- `scripts/moneyclip_sheets.py` — performs runtime actions such as set balance, add expense, get balance, and recap.

Do not rely on browser-based Google Sheets editing as the primary path.

## Linked references

Load only the reference file needed for the current task:

- `references/setup.md` — Google authorization and automatic spreadsheet setup.
- `references/sheets-schema.md` — required Google Sheet tabs and headers.
- `references/runtime.md` — daily expense tracking after setup.
- `references/examples.md` — examples and user guidance.

## Routing

Use only the smallest relevant instruction file.

- If `moneyclip.setup_complete` is not `true`, load `references/setup.md`.
- If Google authorization is missing, run `scripts/google_auth.py` and ask the user to complete the authorization link.
- If no `moneyclip.spreadsheet_id` exists after authorization, run `scripts/create_sheet.py` and save the returned `spreadsheet_id` and `spreadsheet_url`.
- If setup is complete and the user sends balance/spending/recap/edit/delete messages, load `references/runtime.md`.
- If the user asks what the skill can do, load `references/examples.md`.
- Do not read setup instructions during normal daily expense tracking unless setup is incomplete.

## Scope

Use this skill when the message relates to:

- setting cash balance
- recording spending
- checking remaining balance
- daily/weekly/monthly recap
- editing or deleting the last transaction
- setting up MoneyClip storage

Do not use this skill for unrelated personal finance advice, investments, loans, taxes, or banking questions.

## Response principles

- Be brief.
- During runtime, reply in at most two lines.
- Always show remaining balance after a recorded transaction.
- Ask one clear question when setup, Google authorization, or nominal amount is missing.
- Never ask the user to paste Google OAuth secrets into chat. Credential files must stay local.
