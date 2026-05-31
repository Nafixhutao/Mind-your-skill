# Setup Reference

Read this file only when setting up the skill, validating configuration, or troubleshooting Google Sheets access.

## Auth principle

Do not force the user to create a Service Account if Hermes already has usable Google OAuth credentials.

Use the first available working option:

1. Existing Hermes Google Sheets tool authentication.
2. Existing OAuth client flow using `google_client_secret.json` and a stored OAuth token.
3. Existing `GOOGLE_SERVICE_ACCOUNT_JSON` service account credential.
4. New authentication setup only if none of the above works.

## Spreadsheet principle

Do not force the user to provide a Google Sheet ID if Hermes can create a spreadsheet.

Use the first available working option:

1. Use a Sheet URL or Sheet ID if the user already provided one.
2. If `FINANCE_SHEET_ID` is missing and Google auth works, create a new spreadsheet named `Personal Finance Ledger`.
3. Create or validate a tab named `Transactions` unless another tab name is configured.
4. Add the required headers from `references/schema.md`.
5. Save or clearly return the created spreadsheet ID and URL.

Only ask the user for `FINANCE_SHEET_ID` when the runtime cannot create spreadsheets automatically.

## Required user/deployer inputs

Ask for or confirm these non-secret settings only when they are missing and cannot be created automatically:

- Google Sheet ID or permission to create a spreadsheet
- transaction sheet/tab name
- default currency
- default timezone
- preferred category list, if any

Do not ask the user to paste raw client secrets, OAuth tokens, or service account credentials in normal chat.

## Supported authentication modes

### Mode A: Existing Hermes Google Sheets auth

Use this mode when the runtime already has a working Google Sheets integration.

Validate by opening an existing spreadsheet or by creating a small test spreadsheet if no Sheet ID exists and spreadsheet creation is allowed.

### Mode B: OAuth client credentials

Use this mode when the runtime has:

```text
google_client_secret.json
```

or an equivalent configured OAuth client file.

This is valid for user-authorized Google Sheets access if the OAuth flow has completed and a token exists.

Do not ask for a service account if OAuth can access or create spreadsheets.

Recommended config names:

```text
GOOGLE_CLIENT_SECRET_FILE=google_client_secret.json
GOOGLE_OAUTH_TOKEN_FILE=google_token.json
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

The target Google Sheet must be shared with the service account email as Editor, unless the service account created the spreadsheet itself.

## Required config

### `FINANCE_SHEET_ID`

Required after setup, but not required before setup.

If missing and the runtime can create spreadsheets, create a new spreadsheet automatically and then store or report the new ID.

Default spreadsheet title:

```text
Personal Finance Ledger
```

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

## Automatic spreadsheet creation

When Google auth works but no `FINANCE_SHEET_ID` exists:

1. Create a spreadsheet named `Personal Finance Ledger`.
2. Create or rename the first tab to `Transactions`.
3. Add required headers from `references/schema.md`.
4. Freeze the first row if the tool supports it.
5. Return the spreadsheet URL and ID.
6. Ask the runtime to persist `FINANCE_SHEET_ID` if config persistence is available.

If the user explicitly says “buat aja”, “create it”, or similar, create the spreadsheet without asking another confirmation.

If the runtime cannot create a spreadsheet, ask the user to provide an existing Google Sheet URL or ID.

## Setup validation checklist

Setup is valid when:

1. A usable Google auth mode exists: runtime auth, OAuth client + token, or service account.
2. `FINANCE_SHEET_ID` is configured, provided, or newly created.
3. The spreadsheet can be opened.
4. The transaction sheet exists.
5. Required headers match `references/schema.md`.

For OAuth mode, do not require a service account email.

For service account mode, confirm the spreadsheet is shared with the service account email unless the service account created it.

## Required sheet

Default sheet/tab name:

```text
Transactions
```

If the sheet does not exist, create it during setup when the runtime supports sheet modification.

If headers are missing, add them during setup when the runtime supports sheet modification.

## Fallback behavior

If Google Sheets is unavailable:

- Do not pretend the transaction was saved.
- Return the parsed transaction as a draft.
- Tell the user that storage is unavailable.
- Explain whether the problem is missing Sheet ID, missing OAuth token, missing service account, missing spreadsheet-create permission, or access denied.

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

If a new spreadsheet is created:

```text
Saya sudah membuat Google Sheet `Personal Finance Ledger` dan menyiapkan tab `Transactions`. Simpan FINANCE_SHEET_ID ini untuk penggunaan berikutnya: <sheet_id>
```

If optional OCR is unavailable:

```text
Setup Google Sheets selesai. OCR belum tersedia, jadi foto struk perlu diketik manual untuk sementara.
```
