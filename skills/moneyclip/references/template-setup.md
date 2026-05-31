# MoneyClip Template Setup

Use this reference when the user wants the easiest setup path.

This path does not require Google Cloud, OAuth client files, Python, terminal, n8n, or manual tab creation.

## Goal

The user uses a prepared MoneyClip Google Sheet template that already contains:

- `Pengeluaran` tab
- `Saldo` tab
- `State` tab
- MoneyClip Apps Script code

The user only needs to:

1. Make a copy of the template.
2. Deploy the included Apps Script as a Web App.
3. Send the Web App URL back to Hermes.

## First setup message

If `moneyclip.sheet_url` is empty, say:

```text
Buka template MoneyClip, pilih Make a copy, lalu deploy Apps Script sebagai Web App. Setelah itu kirim URL Web App-nya ke sini.
```

If a template URL is configured, include it:

```text
Template MoneyClip:
<moneyclip.template_url>
```

## User steps

Tell the user:

```text
1. Klik template MoneyClip lalu pilih Make a copy.
2. Di Sheet hasil copy: Extensions → Apps Script.
3. Klik Deploy → New deployment → Web app.
4. Set Execute as: Me.
5. Set Who has access: Anyone.
6. Klik Deploy dan izinkan akses Google.
7. Copy Web App URL yang berakhiran /exec.
8. Kirim URL itu ke sini.
```

## When user sends a Web App URL

If the user sends a URL containing `script.google.com/macros/s/`:

1. Treat it as `moneyclip.sheet_url`.
2. Test it by sending action `ping` or `setup`.
3. If response is successful, save `moneyclip.sheet_url`.
4. Set `moneyclip.setup_complete=true`.
5. Reply:

```text
✅ MoneyClip siap.
Sekarang kirim: saldo 200rb
```

## If user sends a normal Google Sheet link

Do not try browser editing as the main path.

Reply:

```text
Link Sheet biasa belum cukup untuk otomatis. MoneyClip butuh Web App URL dari Apps Script supaya bisa mencatat otomatis.
```

Then guide the user back to the template deployment steps.

## If deployment fails

Reply:

```text
Deploy Apps Script belum berhasil. Pastikan pilih Web app, Execute as: Me, dan Who has access: Anyone.
```

## Security

Never ask the user to share Google account password.
Never ask the user to paste private OAuth credentials.
The Web App URL is the configured endpoint for this MoneyClip installation.
