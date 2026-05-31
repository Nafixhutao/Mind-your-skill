# MoneyClip Setup

Use this file only when MoneyClip is not configured yet or when the user asks to set up MoneyClip.

## Setup goal

Prepare MoneyClip storage so Hermes can record expenses automatically.

Default setup path:

1. User copies the MoneyClip Google Sheet template.
2. User deploys the included Apps Script as a Web App.
3. User sends the Web App URL to Hermes.
4. Hermes tests the endpoint and saves `moneyclip.sheet_url`.
5. Hermes sets `moneyclip.setup_complete=true`.

This path does not require Google Cloud OAuth client files, Python, terminal, n8n, or manual tab creation.

## First message

If setup is incomplete and `moneyclip.sheet_url` is empty, load `references/template-setup.md` and guide the user through the template Web App setup.

Say:

```text
Kita pakai setup paling mudah: template MoneyClip + Apps Script Web App. Copy template, deploy Web App, lalu kirim URL /exec ke sini.
```

If `moneyclip.template_url` is configured, include it.

## When the user sends a Web App URL

If the user sends a URL containing:

```text
script.google.com/macros/s/
```

Treat it as `moneyclip.sheet_url`.

Test the endpoint with a lightweight request:

```json
{"action":"ping"}
```

If `ping` is unavailable, test:

```json
{"action":"setup"}
```

If the endpoint responds successfully, save:

```text
moneyclip.sheet_url=<web_app_url>
moneyclip.setup_complete=true
```

Then reply:

```text
✅ MoneyClip siap.
Sekarang kirim: saldo 200rb
```

## If user sends a normal Google Sheet link

Do not rely on browser-based Google Sheets editing as the main path.

Reply:

```text
Link Sheet biasa belum cukup untuk otomatis. MoneyClip butuh Web App URL dari Apps Script supaya bisa mencatat otomatis.
```

Then load `references/template-setup.md`.

## Advanced Google API helper mode

Use the Google Sheets API helper scripts only if the user explicitly chooses advanced/local terminal mode.

Advanced files:

```text
scripts/google_auth.py
scripts/create_sheet.py
scripts/moneyclip_sheets.py
```

Do not mention `client_secret.json` during the default setup unless the user chooses advanced mode.

## If terminal execution is unavailable

For default template setup, terminal is not required. Only HTTP access is needed to call the Web App endpoint after setup.

## Setup should not overwrite data

The Apps Script template must preserve existing data. It may add missing tabs or headers, but it must not delete user data.
