# Examples Reference

Read this file only when examples are requested or runtime behavior is unclear.

## First use with incomplete setup

User:

```text
beli kopi 15rb
```

Assistant:

```text
Saya bisa memahami transaksinya, tetapi Google Sheets belum dikonfigurasi. Periksa setup skill terlebih dahulu sebelum transaksi bisa disimpan.
```

## Normal expense

User:

```text
beli kopi 15rb
```

Parsed:

```json
{
  "type": "expense",
  "amount": 15000,
  "currency": "IDR",
  "category": "Makanan & Minuman",
  "description": "beli kopi",
  "source": "text"
}
```

Assistant:

```text
Tercatat: pengeluaran Rp15.000 untuk Makanan & Minuman.
Deskripsi: beli kopi
```

## Normal income

User:

```text
gajian 5jt
```

Parsed:

```json
{
  "type": "income",
  "amount": 5000000,
  "currency": "IDR",
  "category": "Gaji",
  "description": "gajian",
  "source": "text"
}
```

Assistant:

```text
Tercatat: pemasukan Rp5.000.000 untuk Gaji.
Deskripsi: gajian
```

## Ambiguous amount

User:

```text
bayar belanja 50rb pakai cash 100rb
```

Assistant:

```text
Saya menemukan dua nominal: Rp50.000 dan Rp100.000. Nominal transaksi yang ingin dicatat yang mana?
```

## Missing amount

User:

```text
beli kopi
```

Assistant:

```text
Berapa nominal untuk transaksi beli kopi?
```

## Receipt success

User uploads a receipt image.

OCR result indicates:

```text
Merchant: Indomaret
Total: Rp87.500
```

Assistant:

```text
Struk terbaca dan tercatat: pengeluaran Rp87.500 di Indomaret.
Kategori: Belanja
```

## Receipt low confidence

User uploads a blurry receipt image.

Assistant:

```text
Saya belum yakin membaca total struknya. Tolong ketik total pembayaran dan nama merchant, lalu saya catat.
```

## Monthly summary

User:

```text
ringkasan bulan ini
```

Assistant:

```text
Ringkasan bulan ini:
Saldo: Rp4.250.000
Pemasukan: Rp7.000.000
Pengeluaran: Rp2.750.000
Kategori terbesar: Makanan & Minuman — Rp850.000
```

## Category summary

User:

```text
pengeluaran makan bulan ini
```

Assistant:

```text
Pengeluaran Makanan & Minuman bulan ini: Rp850.000.
```

## Duplicate transaction

User:

```text
beli kopi 15rb
```

Existing similar transaction found today.

Assistant:

```text
Transaksi serupa sudah ada hari ini: Rp15.000 untuk beli kopi. Tetap simpan lagi?
```

## Delete request

User:

```text
hapus transaksi kopi tadi
```

Assistant:

```text
Saya menemukan transaksi Rp15.000 untuk beli kopi hari ini. Konfirmasi: hapus transaksi ini?
```
