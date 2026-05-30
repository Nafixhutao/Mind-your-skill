---
name: moneyclip
description: Telegram expense tracker. Set balance, record spending, and show remaining cash.
version: 4.2.0
metadata:
  hermes:
    tags: [finance, expenses, telegram, google-sheets, indonesia]
    category: productivity
    mode: auto
    trigger: telegram.message
    requires_toolsets: [http]
    config:
      - key: moneyclip.sheet_url
        description: Google Apps Script Web App endpoint
        default: ""
        required: true
      - key: moneyclip.secret_token
        description: Request validation token
        default: ""
        required: true
      - key: moneyclip.timezone
        description: User timezone
        default: Asia/Jakarta
        required: true
---

# MoneyClip

Catat pengeluaran harian dari pesan Telegram.

Prinsip utama: catat pengeluaran, kurangi saldo, tampilkan sisa. Balasan maksimal 2 baris dan selalu tampilkan sisa saldo setelah transaksi.

## Input

Runtime menerima payload berisi `chat_id`, `message_id`, `text`, dan `timestamp`. Field wajib: `chat_id` dan `text`.

## Intent

### Set saldo

Aktif untuk pesan seperti `saldo 200rb`, `pegang 150rb`, `ada uang 1jt`, `cash 300rb`.

Action: `set_balance`.

### Catat pengeluaran

Aktif jika ada aktivitas dan nominal, misalnya `makan 25rb`, `kopi 18k`, `bensin 50rb`, `parkir 5000`, `kemarin beli obat 30rb`.

Action: `add`.

### Cek saldo

Aktif untuk `sisa berapa`, `saldo tinggal berapa`, `cek saldo`, `uangku berapa`.

Action: `get_balance`.

### Rekap

Aktif untuk `rekap`, `rekap hari ini`, `rekap minggu ini`, `rekap bulan ini`.

Action: `recap` dengan period `today`, `week`, atau `month`.

### Edit dan hapus

Edit: `edit makan jadi 20rb`, `ubah yang tadi jadi 15rb`, `transaksi terakhir 50rb`.

Hapus: `hapus yang tadi`, `hapus transaksi terakhir`, `batal catat makan`.

## Jangan catat

Jangan catat jika tidak ada nominal, hanya tanya harga, hanya rencana beli, transaksi batal, ditraktir, dibayarin, nitip, atau ditalangin.

Balasan: `Belum ada yang dicatat.`

## Parsing nominal

- `rb`, `ribu`, `k` dikali 1000.
- `jt`, `juta` dikali 1000000.
- Angka dengan titik atau koma dibaca sebagai rupiah langsung.
- Angka 6 digit atau lebih dibaca apa adanya.
- Aktivitas harian dengan angka kecil diasumsikan ribu.

Contoh: `25rb` menjadi 25000, `25k` menjadi 25000, `1jt` menjadi 1000000, `makan 25` menjadi 25000, `parkir 5` menjadi 5000.

Jika ambigu, tanya: `Nominalnya berapa? pakai rb/jt ya.`

## Tanggal

Default pakai hari ini berdasarkan `moneyclip.timezone`. Jika ada `kemarin`, gunakan H-1. Jika ada `2 hari lalu`, gunakan H-2. Jika ada `3 hari lalu`, gunakan H-3. Format tanggal action: `YYYY-MM-DD`.

## Kategori

- Makanan & Minuman: makan, nasi, kopi, minum, jajan, snack.
- Transport: bensin, parkir, tol, gojek, grab, angkot, bus, kereta.
- Tagihan & Utilitas: listrik, air, pulsa, paket data, wifi, token.
- Kesehatan: obat, dokter, klinik, apotek, vitamin.
- Hiburan & Langganan: nonton, bioskop, spotify, netflix, game.
- Pendidikan: buku, sekolah, kuliah, kelas, kursus.
- Belanja: baju, sepatu, skincare, barang, toko.
- Lainnya: selain kategori di atas.

## Logic khusus

Patungan: jika ada `patungan`, `berdua`, `bertiga`, `berempat`, atau `dibagi X`, catat hanya porsi user. Contoh `patungan makan 90rb bertiga` dicatat 30000.

Cicilan: jika ada kata `cicilan`, tambahkan `(cicilan)` pada deskripsi.

Transfer: jika ada kata `transfer`, tanya `Transfer untuk apa? Mau dicatat sebagai pengeluaran?`

Duplikasi: jika pesan sama atau mirip dengan transaksi terakhir kurang dari 1 menit, tanya `Lanjutan tadi atau transaksi baru?`

## Action contract

Kirim request HTTP POST ke config `moneyclip.sheet_url`. Sertakan token dari config `moneyclip.secret_token` pada payload request.

Set saldo payload: action `set_balance`, `chat_id`, `amount`, `date`.

Catat pengeluaran payload: action `add`, `chat_id`, `message_id`, `date`, dan `entries` berisi `desc`, `amount`, `category`.

Cek saldo payload: action `get_balance`, `chat_id`.

Rekap payload: action `recap`, `chat_id`, `period`.

Edit payload: action `edit`, `chat_id`, `entry_id`, `new_amount`.

Hapus payload: action `delete`, `chat_id`, `entry_id`.

## Format balasan

Set saldo: `💰 Saldo: Rp200.000. Siap!`

Satu transaksi: `✅ makan Rp25.000` lalu `💰 Sisa: Rp175.000`.

Banyak transaksi: `✅ 3 item Rp75.000` lalu `💰 Sisa: Rp125.000`.

Saldo hampir habis: tambah `⚠️ Saldo hampir habis!` jika sisa di bawah 20 persen.

Saldo nol atau minus: tampilkan `🚨 Minus Rp10.000. Mau tambah saldo?`

Cek saldo: `💰 Sisa: Rp125.000` lalu `📉 Keluar: Rp75.000 dari Rp200.000`.

Rekap: `📊 Hari ini — 4 transaksi` lalu `📉 Keluar Rp82.000 | 💰 Sisa Rp118.000`.

## Error

Jika endpoint kosong: `Belum ada endpoint MoneyClip. Setup Google Sheets dulu ya.`

Jika token tidak valid: `Akses MoneyClip belum valid.`

Jika saldo belum diset: `Pegang uang berapa hari ini?`

Jika timeout, retry sekali. Jika tetap gagal: `Gagal simpan. Coba kirim ulang ya.`

## Format sheet

Sheet `Pengeluaran`: ID, Timestamp, Tanggal, Jam, ChatID, MessageID, Deskripsi, Nominal, Kategori.

Sheet `Saldo`: Tanggal, ChatID, Saldo Awal, Total Keluar, Sisa.

Sheet `State`: ChatID, LastMessageID, LastDesc, LastAmount, LastTimestamp, LastEntryID.
