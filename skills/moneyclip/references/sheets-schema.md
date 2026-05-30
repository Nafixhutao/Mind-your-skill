# MoneyClip Google Sheets Schema

Use this file when preparing or repairing MoneyClip storage.

MoneyClip requires three tabs:

1. `Pengeluaran`
2. `Saldo`
3. `State`

Do not delete existing data. Add missing tabs or missing headers only.

## Pengeluaran

Header:

```text
ID | Timestamp | Tanggal | Jam | ChatID | MessageID | Deskripsi | Nominal | Kategori
```

Purpose: stores every recorded expense.

Columns:

- `ID`: unique transaction ID
- `Timestamp`: ISO timestamp when recorded
- `Tanggal`: transaction date in `YYYY-MM-DD`
- `Jam`: transaction time in `HH:mm:ss`
- `ChatID`: Telegram or Hermes chat identifier
- `MessageID`: source message ID when available
- `Deskripsi`: expense description
- `Nominal`: amount in rupiah as integer
- `Kategori`: inferred category

## Saldo

Header:

```text
Tanggal | ChatID | Saldo Awal | Total Keluar | Sisa
```

Purpose: stores current balance summary per chat/user.

Columns:

- `Tanggal`: date when balance was set or updated
- `ChatID`: Telegram or Hermes chat identifier
- `Saldo Awal`: starting balance in rupiah
- `Total Keluar`: total recorded spending
- `Sisa`: remaining balance

## State

Header:

```text
ChatID | LastMessageID | LastDesc | LastAmount | LastTimestamp | LastEntryID
```

Purpose: stores lightweight runtime state for duplicate detection and edit/delete last transaction.

Columns:

- `ChatID`: Telegram or Hermes chat identifier
- `LastMessageID`: last processed message ID
- `LastDesc`: last expense description
- `LastAmount`: last expense amount
- `LastTimestamp`: timestamp of the last processed transaction
- `LastEntryID`: ID of the last recorded expense

## Setup success criteria

Setup is successful when all three tabs exist and all headers match the required schema.

After setup, reply:

```text
✅ Sheet MoneyClip siap.
Sekarang kirim: saldo 200rb
```
