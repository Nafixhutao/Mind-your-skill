# Setup Reference

Read this file only when setting up the skill, validating configuration, or troubleshooting Google Sheets access.

## Auth principle

Do not force the user to create a Service Account if Hermes already has usable Google OAuth credentials.

Use the first available working option:

1. Existing Hermes Google Sheets tool authentication.
2. Existing OAuth client flow using `google_client_secret.json` and a stored OAuth token.
3. Existing `GOOGLE_SERVICE_ACCOUNT_JSON` service account credential.
4. New authentication setup only if none of the above works.

## Required user/deployer inputs

Ask for or confirm these non-secret settings:

- Google Sheet ID
- transaction sheet/tab name
- default currency
- default timezone
- preferred category list, if any

Do not ask the user to paste raw client secrets, OAuth tokens, or service account credentials in normal chat.

## Supported authentication modes

### Mode A: Existing Hermes Google Sheets auth

Use this mode when the runtime already has a working Google Sheets integration.

Validate by opening the spreadsheet from `FINANCE_SHEET_ID` or a user-provided Sheet URL.

### Mode B: OAuth client credentials

Use this mode when the runtime has:

```text
google_client_secret.json
```

or an equivalent configured OAuth client file.

This is valid for user-authorized Google Sheets access if the OAuth flow has completed and a token exists.

Do not ask for a service account if OAuth can access the spreadsheet.

Recommended config names:

```text
GOOGLE_CLIENT_SECRET_FILE=google_client_secret.json
GOOGLE_OAUTH_TOKEN_FILE=token.json
```

The exact token path may depend on the Hermes runtime.

### Mode C: Service Account credentials

Use this mode only when service account credentials already exist or the user explicitly chooses service account setup.

Environment variable:

```text
GOOGLE_SERVICE_ACCOUNT_JSON
```

Contains the Google Service Account credentials JSON.

Recommended formats:

1. raw JSON string, or
2. base64-encoded JSON string if the runtime supports decoding.

The skill must never print this value.

The target Google Sheet must be shared with the service account email as Editor.

## Required config

### `FINANCE_SHEET_ID`

Required unless the user provides a Google Sheet URL and the runtime can extract the ID.

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

## Setup validation checklist

Setup is valid when:

1. A usable Google auth mode exists: runtime auth, OAuth client + token, or service account.
2. `FINANCE_SHEET_ID` is configured or a Sheet URL is provided.
3. The spreadsheet can be opened.
4. The transaction sheet exists.
5. Required headers match `references/schema.md`.

For OAuth mode, do not require a service account email.

For service account mode, confirm the spreadsheet is shared with the service account email.

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
- Explain whether the problem is missing Sheet ID, missing OAuth token, missing service account, or access denied.

If OCR is unavailable:

- Ask the user to type the total and merchant manually.
- Do not block text-based transaction recording.

## Setup completion response

When setup is valid, respond briefly:

```text
Setup selesai. Skill siap mencatat transaksi ke Google Sheets.
```

If OAuth is used:

```text
Setup selesai memakai OAuth Google yang sudah ada. Skill siap mencatat transaksi ke Google Sheets.
```

If optional OCR is unavailable:

```text
Setup Google Sheets selesai. OCR belum tersedia, jadi foto struk perlu diketik manual untuk sementara.
```
