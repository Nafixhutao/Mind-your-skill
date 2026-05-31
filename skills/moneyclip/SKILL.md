---
name: moneyclip
description: Personal expense tracking skill for Hermes Agent. Uses a MoneyClip Google Sheet template with Apps Script Web App endpoint for easy setup, then tracks balance and spending from chat messages.
version: 4.8.0
metadata:
  hermes:
    tags: [finance, expense-tracker, telegram, google-sheets, indonesia]
    category: productivity
    mode: auto
    trigger: telegram.message
    requires_toolsets: [http]
    optional_toolsets: [terminal]
    config:
      - key: moneyclip.sheet_url
        description: Google Apps Script Web App endpoint from the copied MoneyClip template.
        default: ""
        required: false
      - key: moneyclip.template_url
        description: Optional MoneyClip Google Sheet template copy URL.
        default: ""
        required: false
      - key: moneyclip.spreadsheet_id
        description: Optional Google Spreadsheet ID for advanced Google API helper mode.
        default: ""
        required: false
      - key: moneyclip.spreadsheet_url
        description: Optional Google Spreadsheet URL for advanced Google API helper mode.
        default: ""
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

1. **Setup phase** — guide the user to copy the MoneyClip Google Sheet template, deploy the included Apps Script as a Web App, and save the Web App URL.
2. **Runtime phase** — parse balance/spending messages, send actions to the configured Web App endpoint, and reply with the remaining balance.

## Primary setup path

Use the template Apps Script path first. This is the easiest path for normal users because it does not require Google Cloud OAuth client files, Python, terminal, n8n, or manual tab creation.

Primary storage config:

`moneyclip.sheet_url`

This should be a Google Apps Script Web App URL ending in `/exec`.

## Advanced setup path

If the user explicitly wants local Google Sheets API mode and terminal execution is available, the helper scripts in `scripts/` may be used:

- `scripts/google_auth.py`
- `scripts/create_sheet.py`
- `scripts/moneyclip_sheets.py`

Do not use advanced Google API helper mode unless the user chooses it.

## Linked references

Load only the reference file needed for the current task:

- `references/setup.md` — setup router and recommended path.
- `references/template-setup.md` — easiest template Apps Script setup.
- `references/apps-script.md` — Apps Script Web App code/reference.
- `references/sheets-schema.md` — required Google Sheet tabs and headers.
- `references/runtime.md` — daily expense tracking after setup.
- `references/examples.md` — examples and user guidance.

## Routing

Use only the smallest relevant instruction file.

- If `moneyclip.setup_complete` is not `true`, load `references/setup.md`.
- If setup is incomplete and the user is normal/non-technical, load `references/template-setup.md`.
- If the user sends a Google Apps Script Web App URL, test and save it as `moneyclip.sheet_url`.
- If setup is complete and the user sends balance/spending/recap/edit/delete messages, load `references/runtime.md`.
- If the user asks for Apps Script code or template internals, load `references/apps-script.md`.
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
- Ask one clear question when setup, endpoint URL, or nominal amount is missing.
- Never ask for Google account passwords or private OAuth credentials.
