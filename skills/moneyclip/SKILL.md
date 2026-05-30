---
name: moneyclip
description: Personal expense tracking skill for Hermes Agent. Guides first-run Google Sheet setup, then tracks balance and spending from Telegram messages.
version: 4.4.0
metadata:
  hermes:
    tags: [finance, expense-tracker, telegram, google-sheets, indonesia]
    category: productivity
    mode: auto
    trigger: telegram.message
    requires_toolsets: [http, browser]
    config:
      - key: moneyclip.sheet_link
        description: Google Sheet link used by setup flow.
        default: ""
        required: false
      - key: moneyclip.sheet_url
        description: Optional Google Apps Script Web App endpoint.
        default: ""
        required: false
      - key: moneyclip.secret_token
        description: Optional request validation token for endpoint mode.
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

MoneyClip is a Hermes Agent skill for personal daily expense tracking in Indonesian chat style.

It has two phases:

1. **Setup phase** — ask for a Google Sheet link, prepare the required tabs, and mark setup as complete.
2. **Runtime phase** — parse balance/spending messages, update storage, and reply with the remaining balance.

## Routing

Use only the smallest relevant instruction file.

- If `moneyclip.setup_complete` is not `true`, use `setup.md`.
- If the user sends a Google Sheet link, use `setup.md` and `sheets-schema.md`.
- If setup is complete and the user sends balance/spending/recap/edit/delete messages, use `runtime.md`.
- If the user asks what the skill can do, use `examples.md`.
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
- Ask one clear question when setup or nominal amount is missing.
