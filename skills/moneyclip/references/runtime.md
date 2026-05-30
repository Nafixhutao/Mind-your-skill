# MoneyClip Runtime

Use this file only after MoneyClip setup is complete.

## Core behavior

MoneyClip tracks daily cash spending.

Flow:

1. Detect intent.
2. Parse amount.
3. Infer category.
4. Store the action.
5. Reply with the remaining balance.

During runtime, reply in at most two lines.

## Active intents

### Set balance

Examples:

- `saldo 200rb`
- `saldo awal 500rb`
- `pegang 150rb`
- `ada uang 1jt`
- `cash 300rb`

Action: `set_balance`.

Reply:

```text
💰 Saldo: Rp200.000. Siap!
```

### Add expense

Active when the message contains an activity and an amount.

Examples:

- `makan 25rb`
- `kopi 18k`
- `bensin 50rb`
- `parkir 5000`
- `kemarin beli obat 30rb`

Action: `add`.

Reply:

```text
✅ makan Rp25.000
💰 Sisa: Rp175.000
```

### Check balance

Examples:

- `sisa berapa`
- `saldo tinggal berapa`
- `cek saldo`
- `uangku berapa`

Action: `get_balance`.

Reply:

```text
💰 Sisa: Rp125.000
📉 Keluar: Rp75.000 dari Rp200.000
```

### Recap

Examples:

- `rekap`
- `rekap hari ini`
- `rekap minggu ini`
- `rekap bulan ini`

Action: `recap` with period `today`, `week`, or `month`.

Reply:

```text
📊 Hari ini — 4 transaksi
📉 Keluar Rp82.000 | 💰 Sisa Rp118.000
```

### Edit or delete

Edit examples:

- `edit makan jadi 20rb`
- `ubah yang tadi jadi 15rb`
- `transaksi terakhir 50rb`

Delete examples:

- `hapus yang tadi`
- `hapus transaksi terakhir`
- `batal catat makan`

Use the last entry from state if no entry ID is provided.

## Do not record

Do not record if the user:

- gives no amount
- only asks a price
- only plans to buy something
- says the purchase was cancelled
- says someone else paid
- says it was entrusted, borrowed, or covered by someone else

Reply:

```text
Belum ada yang dicatat.
```

## Amount parsing

- `rb`, `ribu`, `k` = x1000
- `jt`, `juta` = x1000000
- dotted or comma numbers are read as rupiah directly
- numbers with 6 or more digits are read as-is
- small numbers in daily contexts are treated as thousands

Examples:

- `25rb` → 25000
- `25k` → 25000
- `1jt` → 1000000
- `makan 25` → 25000
- `parkir 5` → 5000

If ambiguous, ask:

```text
Nominalnya berapa? pakai rb/jt ya.
```

## Dates

Default date is today in `moneyclip.timezone`.

- `kemarin` = previous day
- `2 hari lalu` = two days ago
- `3 hari lalu` = three days ago
- `tadi lupa` or `lupa catat` = use the intended date if clear, otherwise today

Action date format: `YYYY-MM-DD`.

## Categories

- Makanan & Minuman: makan, nasi, kopi, minum, jajan, snack
- Transport: bensin, parkir, tol, gojek, grab, angkot, bus, kereta
- Tagihan & Utilitas: listrik, air, pulsa, paket data, wifi, token
- Kesehatan: obat, dokter, klinik, apotek, vitamin
- Hiburan & Langganan: nonton, bioskop, spotify, netflix, game
- Pendidikan: buku, sekolah, kuliah, kelas, kursus
- Belanja: baju, sepatu, skincare, barang, toko
- Lainnya: everything else

## Special cases

Patungan: if the message says `patungan`, `berdua`, `bertiga`, `berempat`, or `dibagi X`, record only the user's share.

Cicilan: if the message contains `cicilan`, add `(cicilan)` to the description.

Transfer: if the message contains `transfer`, ask:

```text
Transfer untuk apa? Mau dicatat sebagai pengeluaran?
```

Duplicate: if the message is the same or very similar to the previous transaction within one minute, ask:

```text
Lanjutan tadi atau transaksi baru?
```

## Storage

If `moneyclip.sheet_url` exists, send the matching action payload by HTTP POST.

If direct Google Sheet editing is available, write directly to the tabs defined in `references/sheets-schema.md`.

Never hardcode secrets. Use configured values only.

## Errors

If setup is incomplete:

```text
Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.
```

If balance is missing:

```text
Pegang uang berapa hari ini?
```

If endpoint or token is invalid:

```text
Akses MoneyClip belum valid.
```

If storage times out, retry once. If it still fails:

```text
Gagal simpan. Coba kirim ulang ya.
```
