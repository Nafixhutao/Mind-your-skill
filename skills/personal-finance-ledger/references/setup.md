# Setup Reference

Read this file only when setting up the skill, validating configuration, or troubleshooting Google Sheets access.

## Required user/deployer inputs

Ask for or confirm these non-secret settings:

- Google Sheet ID
- transaction sheet/tab name
- default currency
- default timezone
- preferred category list, if any

Do not ask the user to paste raw service account credentials in normal chat.

## Required environment variables

### `GOOGLE_SERVICE_ACCOUNT_JSON`

Required.

Contains the Google Service Account credentials JSON.

Recommended formats:

1. raw JSON string, or
2. base64-encoded JSON string if the runtime supports decoding.

The skill must never print this value.

### `FINANCE_SHEET_ID`

Required unless supplied by another secure config channel.

The ID of the Google Spreadsheet used for storage.

### `FINANCE_TRANSACTIONS_SHEET_NAME`

Optional.

Default:

```text
Transactions
```

### `FINANCE_DEFAULT_CURRENCY`

Optional.

Default:

```text
IDR
```

### `FINANCE_DEFAULT_TIMEZONE`

Optional.

Default:

```text
Asia/Jakarta
```

## Google Sheets permission setup

The target Google Sheet must be shared with the service account email.

Minimum recommended permission:

```text
Editor
```

Only share the specific spreadsheet needed by this skill.

Do not grant broad Google Drive access unless the runtime explicitly requires it.

## Setup validation checklist

Setup is valid when:

1. `GOOGLE_SERVICE_ACCOUNT_JSON` exists.
2. The service account JSON can be parsed.
3. The service account email is present in the JSON.
4. `FINANCE_SHEET_ID` is configured.
5. The spreadsheet can be opened.
6. The transaction sheet exists.
7. Required headers match `references/schema.md`.

## Required sheet

Default sheet/tab name:

```text
Transactions
```

If the sheet does not exist, ask permission before creating it.

If headers are missing, ask permission before adding or modifying headers.

## Fallback behavior

If Google Sheets is unavailable:

- Do not pretend the transaction was saved.
- Return the parsed transaction as a draft.
- Tell the user that storage is unavailable.
- Ask the user to retry after setup is fixed.

If OCR is unavailable:

- Ask the user to type the total and merchant manually.
- Do not block text-based transaction recording.

## Setup completion response

When setup is valid, respond briefly:

```text
Setup selesai. Skill siap mencatat transaksi ke Google Sheets.
```

If optional OCR is unavailable:

```text
Setup Google Sheets selesai. OCR belum tersedia, jadi foto struk perlu diketik manual untuk sementara.
```
