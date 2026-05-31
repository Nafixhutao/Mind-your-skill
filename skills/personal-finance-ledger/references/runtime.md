# Runtime Reference

Read this file for daily use.

## Supported intents

Detect the user intent:

1. `record_expense`
2. `record_income`
3. `record_receipt_expense`
4. `show_balance_summary`
5. `show_category_summary`
6. `show_transactions`
7. `update_transaction`
8. `delete_transaction`
9. `setup_check`

## Intent detection

### Record expense

Examples:

```text
beli kopi 15rb
bayar listrik 350000
makan siang 42k
grab 28rb
```

Default to expense when the text indicates spending, buying, paying, or transfer out.

### Record income

Examples:

```text
gajian 5jt
dapat bonus 750rb
freelance project 2 juta
```

Default to income when the text indicates salary, payment received, bonus, refund, or money in.

### Receipt expense

Activate when the user uploads or references a receipt, nota, invoice, or payment screenshot.

Treat receipt transactions as expenses unless the user clearly says it is a refund or income.

### Summary

Examples:

```text
saldo bulan ini
pengeluaran minggu ini
ringkasan Mei 2026
kategori terbesar bulan ini
```

## Parsing free-text transactions

Extract:

- `type`: `income` or `expense`
- `amount`
- `currency`
- `description`
- `merchant`
- `category`
- `transaction_date`
- `source`

Default values:

- `currency`: configured default currency
- `transaction_date`: today in configured timezone
- `source`: `text`

## Amount parsing rules

Support common Indonesian shorthand:

```text
15rb = 15000
15k = 15000
5jt = 5000000
5 juta = 5000000
1.250.000 = 1250000
1,250,000 = 1250000
```

If multiple amounts appear and intent is unclear, ask which amount to record.

Do not record transactions without an amount.

## Category inference

Infer category from description and merchant.

Default categories:

- Makanan & Minuman
- Transportasi
- Belanja
- Tagihan
- Rumah
- Kesehatan
- Pendidikan
- Hiburan
- Gaji
- Bonus
- Freelance
- Transfer
- Refund
- Lainnya

Use `Lainnya` if confidence is low but the transaction is otherwise clear.

Ask only if category materially affects the user request.

## Receipt OCR handling

When a receipt image is provided:

1. Run OCR if available.
2. Extract merchant name.
3. Extract total amount.
4. Detect date if visible.
5. Infer category.
6. Save as expense if confidence is sufficient.

Prefer fields labeled:

```text
TOTAL
Grand Total
Jumlah
Total Bayar
Amount
Paid
```

Avoid using subtotal, tax, discount, change, or cash received as the final amount unless clearly indicated.

## Receipt confidence rules

Ask for confirmation when:

- no total is detected,
- multiple possible totals conflict,
- OCR text is unreadable,
- merchant is missing and category is unclear,
- detected amount seems implausible.

Example:

```text
Saya menemukan dua kemungkinan total: Rp78.000 dan Rp100.000. Yang mana yang ingin dicatat?
```

## Google Sheets write behavior

Use append-only writes for new transactions.

Before appending, validate required fields:

- transaction_id
- transaction_date
- type
- amount
- currency
- category
- description
- source
- created_at

Do not overwrite existing rows during normal recording.

## Duplicate handling

Potential duplicate if all match:

- same date,
- same amount,
- same merchant or description,
- same source within a short time window.

If likely duplicate, ask before saving:

```text
Transaksi serupa sudah ada hari ini: Rp15.000 untuk Kopi. Tetap simpan lagi?
```

## Summary behavior

For summaries:

1. Read rows from Google Sheets.
2. Filter by requested date range.
3. Sum income.
4. Sum expense.
5. Calculate balance:

```text
balance = total_income - total_expense
```

6. Group expenses by category if requested.

Default date range:

- If user says “bulan ini”: current calendar month.
- If user says “minggu ini”: current week.
- If user gives no range: current calendar month.

## Response format

### Saved expense

```text
Tercatat: pengeluaran Rp15.000 untuk Makanan & Minuman.
Deskripsi: beli kopi
```

### Saved income

```text
Tercatat: pemasukan Rp5.000.000 untuk Gaji.
Deskripsi: gajian
```

### Receipt saved

```text
Struk terbaca dan tercatat: pengeluaran Rp87.500 di Indomaret.
Kategori: Belanja
```

### Summary

```text
Ringkasan bulan ini:
Saldo: Rp4.250.000
Pemasukan: Rp7.000.000
Pengeluaran: Rp2.750.000
Kategori terbesar: Makanan & Minuman — Rp850.000
```

## When to ask follow-up questions

Ask only when required.

Ask if:

- amount is missing,
- transaction type cannot be inferred,
- receipt total is ambiguous,
- user asks to edit/delete but target transaction is unclear,
- Google Sheets setup is incomplete.

Do not ask if:

- only category is uncertain; use `Lainnya`,
- merchant is missing but description is clear,
- date is missing; use today,
- currency is missing; use configured default.

## Confirmation rules

Require confirmation before:

- deleting transactions,
- editing existing transactions,
- bulk changes,
- creating or modifying sheet headers,
- saving likely duplicates,
- recording low-confidence receipt extraction.

No confirmation needed for a clear new transaction append.

## Error handling

### Missing setup

```text
Belum bisa menyimpan transaksi karena Google Sheets belum dikonfigurasi. Periksa setup skill terlebih dahulu.
```

### Sheets write failure

```text
Transaksi berhasil dipahami, tetapi gagal disimpan ke Google Sheets. Data belum tercatat.
```

### OCR unavailable

```text
OCR belum tersedia. Tolong ketik total dan nama merchant dari struk, lalu saya catat.
```

### Invalid amount

```text
Saya belum menemukan nominal transaksi. Berapa jumlahnya?
```

## Safety boundaries

This skill may summarize records, but must not provide professional financial, investment, tax, or legal advice.

Allowed:

```text
Pengeluaran makan bulan ini Rp850.000.
```

Not allowed as definitive advice:

```text
Kamu harus membeli saham ini.
```

For advice-like requests, respond with a non-professional framing and suggest consulting a qualified expert when appropriate.
