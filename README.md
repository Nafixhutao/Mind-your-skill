# Mind Your Skill

Repository ini berisi skill **MoneyClip**, yaitu pencatat pengeluaran harian untuk Telegram.

## MoneyClip

MoneyClip membantu user mencatat uang keluar dari chat Telegram.

Contoh pesan:

```text
saldo 200rb
makan 25rb
bensin 50rb
kemarin beli obat 30rb
sisa berapa
rekap hari ini
```

Contoh balasan:

```text
✅ makan Rp25.000
💰 Sisa: Rp175.000
```

## File

- `moneyclip.skill.md` — file skill utama.
- `README.md` — tutorial dan penjelasan repo.

## Cara Kerja

Skill ini adalah aturan/otak MoneyClip. Agar berjalan otomatis, skill perlu dipasang ke runner atau webhook Telegram.

Flow ideal:

```text
User kirim pesan Telegram
→ Telegram Bot Webhook
→ Runner membaca moneyclip.skill.md
→ Runner parsing pesan
→ Runner kirim action ke Google Apps Script
→ Google Sheets update
→ Bot balas sisa saldo
```

## Config yang Dibutuhkan

```yaml
moneyclip.sheet_url: "URL Google Apps Script Web App"
moneyclip.secret_token: "token rahasia untuk validasi request"
moneyclip.timezone: "Asia/Jakarta"
```

## Format Google Sheets

Buat 3 sheet.

### Pengeluaran

```text
ID | Timestamp | Tanggal | Jam | ChatID | MessageID | Deskripsi | Nominal | Kategori
```

### Saldo

```text
Tanggal | ChatID | Saldo Awal | Total Keluar | Sisa
```

### State

```text
ChatID | LastMessageID | LastDesc | LastAmount | LastTimestamp | LastEntryID
```

## Catatan Penting

Skill tidak otomatis berjalan hanya karena file ada di GitHub. Otomatisasi membutuhkan:

- Telegram Bot
- Webhook atau runner
- Google Apps Script endpoint
- Google Sheets

Setelah komponen itu tersambung, user tinggal kirim pesan Telegram dan MoneyClip akan mencatat otomatis.
