# MoneyClip Setup

Use this file only when MoneyClip is not configured yet or when the user asks to set up MoneyClip.

## Setup goal

Prepare MoneyClip storage automatically through Google Sheets API helper scripts.

Preferred setup path:

1. Authorize Google Sheets API once.
2. Create a new MoneyClip Google Sheet automatically.
3. Prepare required tabs and headers.
4. Save `moneyclip.spreadsheet_id` and `moneyclip.spreadsheet_url`.
5. Mark `moneyclip.setup_complete=true`.

Do not rely on browser-based Google Sheets editing as the primary path.

## Requirements

Hermes needs terminal/script execution and Python dependencies from:

```text
skills/moneyclip/scripts/requirements.txt
```

Install if needed:

```bash
pip install -r skills/moneyclip/scripts/requirements.txt
```

The user also needs a local Google OAuth Desktop Client file at:

```text
~/.moneyclip/client_secret.json
```

Never ask the user to paste OAuth secrets into chat. The credential file must stay local.

## First message

If setup is incomplete, say:

```text
Saya akan menyiapkan Google Sheet MoneyClip otomatis. Saya perlu izin Google Sheets sekali. Siapkan file OAuth client di ~/.moneyclip/client_secret.json, lalu saya jalankan authorization.
```

If the user has not prepared the OAuth client file, say:

```text
Buat OAuth Desktop Client di Google Cloud, download sebagai client_secret.json, lalu simpan di ~/.moneyclip/client_secret.json. Jangan kirim file itu ke chat.
```

## Authorization

Run:

```bash
python skills/moneyclip/scripts/google_auth.py
```

The script will open or print a Google authorization link. Ask the user to open it, choose their Google account, and allow access.

After authorization succeeds, the script stores token locally at:

```text
~/.moneyclip/token.json
```

Do not commit `client_secret.json` or `token.json` to GitHub.

## Create Sheet automatically

After authorization succeeds, run:

```bash
python skills/moneyclip/scripts/create_sheet.py
```

The script returns JSON containing:

```json
{
  "ok": true,
  "spreadsheet_id": "...",
  "spreadsheet_url": "https://docs.google.com/spreadsheets/d/.../edit"
}
```

Save:

```text
moneyclip.spreadsheet_id=<spreadsheet_id>
moneyclip.spreadsheet_url=<spreadsheet_url>
moneyclip.setup_complete=true
```

Then reply:

```text
✅ MoneyClip siap. Sheet sudah dibuat otomatis.
Sekarang kirim: saldo 200rb
```

## If authorization fails

Reply:

```text
Authorization Google belum berhasil. Cek file ~/.moneyclip/client_secret.json lalu coba lagi.
```

## If terminal execution is unavailable

Reply:

```text
Mode ini butuh terminal untuk menjalankan Google Sheets API helper. Jalankan setup di perangkat yang bisa menjalankan Python.
```

## Setup should not overwrite data

If the user already has an existing MoneyClip spreadsheet ID, do not create a new spreadsheet unless the user asks for a fresh setup.

If using an existing spreadsheet, run `scripts/moneyclip_sheets.py` with action `setup` to repair missing headers.
