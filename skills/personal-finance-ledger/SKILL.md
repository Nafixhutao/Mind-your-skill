---
name: personal-finance-ledger
description: Track personal income and expenses from free text or receipt images, then save them to Google Sheets.
version: 1.0.2
metadata:
  hermes:
    tags:
      - finance
      - expense-tracking
      - google-sheets
      - ocr
      - productivity
    category: productivity
    requires_toolsets:
      - google_sheets
    optional_toolsets:
      - ocr
      - file_input
    config:
      - FINANCE_SHEET_ID
      - FINANCE_TRANSACTIONS_SHEET_NAME
      - FINANCE_DEFAULT_CURRENCY
      - FINANCE_DEFAULT_TIMEZONE
      - GOOGLE_CLIENT_SECRET_FILE
      - GOOGLE_OAUTH_TOKEN_FILE
    optional_environment_variables:
      - GOOGLE_SERVICE_ACCOUNT_JSON
---

# Personal Finance Ledger Skill

Use this skill when the user wants to record, inspect, or summarize personal income and expense transactions.

## Activate when

- The user gives a money transaction in free text.
- The user uploads or references a receipt, nota, or struk.
- The user asks for balance, income, expense, or category summaries.
- The user wants transaction data saved to Google Sheets.

## Do not activate when

- The user asks for investment, tax, legal, or financial advice beyond basic record keeping.
- The user wants business accounting, invoicing, payroll, or tax filing.
- The user asks to delete or overwrite financial data without explicit confirmation.
- No usable Google Sheets authentication is available.

## Google auth priority

Use existing Google authentication before asking the user to create anything new.

Preferred order:

1. Existing OAuth client flow, such as `google_client_secret.json` plus a valid OAuth token.
2. Existing Google Sheets tool authentication provided by the Hermes runtime.
3. Existing `GOOGLE_SERVICE_ACCOUNT_JSON` service account credential.
4. Only if none are available, ask the user to set up Google authentication.

Do not ask for a service account if OAuth credentials already exist and can access Google Sheets.

## Spreadsheet setup priority

If Google auth works but `FINANCE_SHEET_ID` is missing, do not immediately ask the user for a Sheet ID.

Preferred order:

1. If the user provided a Google Sheet URL or ID, use it.
2. If no Sheet is provided and the runtime can create Google Sheets, offer to create a new spreadsheet named `Personal Finance Ledger`.
3. If the user already said to create it, create it without asking again.
4. Create or validate the `Transactions` tab and required headers from `references/schema.md`.
5. Save or report the new `FINANCE_SHEET_ID` for future runs.

Only ask the user for an existing Sheet ID if the runtime cannot create a spreadsheet.

## Reference routing

Read only what is needed:

- `references/runtime.md` for daily transaction handling and summaries.
- `references/setup.md` only during setup or configuration issues.
- `references/schema.md` when validating, writing, or reading sheet rows.
- `references/examples.md` only when examples are requested or behavior is unclear.

## Response principles

- Keep responses short and clear.
- Confirm saved transactions with amount, type, category, and date.
- Ask follow-up questions only when required data is missing or confidence is low.
- Prefer append-only writes.
- Never expose credentials, OAuth tokens, client secrets, or service account JSON.

## Security limits

- Do not request secrets through normal chat.
- Do not hardcode credentials.
- Do not send financial data to unknown endpoints.
- Require confirmation before editing, deleting, or bulk-modifying data.
- Treat receipt images and financial records as sensitive personal data.
