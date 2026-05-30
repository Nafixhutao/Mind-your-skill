# MoneyClip Setup

Use this file only when MoneyClip is not configured yet, when the user asks to set up MoneyClip, or when the user sends a Google Sheet link.

## Setup goal

Prepare storage so MoneyClip can track balance and expenses.

Minimum setup is complete when either:

- Hermes can directly edit the user's Google Sheet from `moneyclip.sheet_link`, or
- `moneyclip.sheet_url` points to a working endpoint that stores MoneyClip actions.

## First message

If no sheet link or endpoint is configured, ask:

```text
Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.
```

If the user does not have a sheet yet, say:

```text
Buat Google Sheet baru, share Anyone with the link sebagai Editor, lalu kirim linknya ke sini.
```

## When the user sends a Google Sheet link

1. Treat the link as `moneyclip.sheet_link`.
2. Open the sheet if Hermes has a browser or Google Sheets tool.
3. Check whether edit access is available.
4. Create or repair the required tabs using `sheets-schema.md`.
5. If config persistence is available, save `moneyclip.sheet_link` and set `moneyclip.setup_complete=true`.
6. Reply:

```text
✅ Sheet MoneyClip siap.
Sekarang kirim: saldo 200rb
```

## If edit access is denied

Reply:

```text
Belum bisa edit Sheet. Ubah akses ke Anyone with the link → Editor, lalu kirim ulang linknya.
```

## If Hermes cannot edit Google Sheets directly

Reply:

```text
Saya belum bisa mengedit Sheet langsung di mode ini. Saya pandu setup manualnya ya.
```

Then show the required tabs and headers from `sheets-schema.md`.

## Endpoint mode

If Hermes requires HTTP storage instead of direct Sheet editing, MoneyClip needs `moneyclip.sheet_url`.

If the endpoint is missing after the sheet is prepared, say:

```text
Sheet sudah siap. Untuk simpan otomatis, MoneyClip butuh Apps Script Web App endpoint.
```

If Hermes can create Apps Script automatically, create the endpoint and save it as `moneyclip.sheet_url`.

If not, ask the user to provide the endpoint.

## Setup should not overwrite data

If a required tab already exists, do not delete it. Only add missing headers or missing tabs.

If existing data is present, preserve it.
