---
name: moneyclip
description: Telegram expense tracker with first-run setup wizard. Ask for Google Sheet link, prepare sheet columns, then track spending automatically.
version: 4.3.0
metadata:
  hermes:
    tags: [finance, expenses, telegram, google-sheets, indonesia, setup-wizard]
    category: productivity
    mode: auto
    trigger: telegram.message
    requires_toolsets: [http, browser]
    config:
      - key: moneyclip.sheet_url
        description: Google Apps Script Web App endpoint. Optional during first setup.
        default: ""
        required: false
      - key: moneyclip.sheet_link
        description: Google Sheet link. Used by setup wizard to prepare tabs and headers.
        default: ""
        required: false
      - key: moneyclip.secret_token
        description: Request validation token.
        default: ""
        required: false
      - key: moneyclip.timezone
        description: User timezone.
        default: Asia/Jakarta
        required: true
      - key: moneyclip.setup_complete
        description: Whether MoneyClip setup is finished.
        default: "false"
        required: false
---

# MoneyClip

MoneyClip adalah skill pencatat pengeluaran harian dari pesan Telegram.

Tujuan utama:
- Saat user pertama kali memakai skill, bantu setup dulu.
- Jika belum ada Google Sheet, tanya link Google Sheet.
- Jika user memberi link Google Sheet, siapkan tab dan header MoneyClip.
- Setelah setup selesai, catat pengeluaran, kurangi saldo, dan tampilkan sisa.

Balasan ke user maksimal 2 baris kecuali saat setup awal.

---

## First-run setup wizard

Skill harus menjalankan setup wizard jika salah satu kondisi ini terjadi:

- `moneyclip.setup_complete` belum `true`.
- `moneyclip.sheet_link` kosong dan `moneyclip.sheet_url` kosong.
- User berkata `setup moneyclip`, `atur moneyclip`, `mulai moneyclip`, atau `pakai moneyclip`.
- User mengirim link Google Sheet.

### Langkah 1 — minta link Google Sheet

Jika belum ada link Google Sheet atau endpoint, jangan langsung mencatat transaksi. Tanya:

`Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.`

Jika user belum punya sheet, arahkan singkat:

`Buat Google Sheet baru, share Anyone with the link sebagai Editor, lalu kirim linknya ke sini.`

### Langkah 2 — saat user memberi link Google Sheet

Jika user mengirim URL Google Sheet:

1. Simpan sebagai `moneyclip.sheet_link` jika Hermes mendukung penyimpanan config/memory.
2. Buka Google Sheet tersebut jika tool browser/sheets tersedia.
3. Pastikan akses edit tersedia.
4. Buat atau rapikan 3 tab: `Pengeluaran`, `Saldo`, `State`.
5. Isi header sesuai format MoneyClip.
6. Setelah selesai, balas:

`✅ Sheet MoneyClip siap.`
`Sekarang kirim: saldo 200rb`

Jika tidak bisa mengedit karena akses ditolak, balas:

`Belum bisa edit Sheet. Ubah akses ke Anyone with the link → Editor, lalu kirim ulang linknya.`

Jika Hermes tidak punya tool untuk mengedit Google Sheet langsung, balas:

`Saya belum bisa mengedit Sheet langsung di mode ini. Saya pandu setup manualnya ya.`

Lalu beri 3 header sheet yang harus dibuat.

### Langkah 3 — endpoint Apps Script

Jika runtime membutuhkan `moneyclip.sheet_url` untuk menyimpan data, dan endpoint belum ada, jelaskan singkat:

`Sheet sudah siap. Untuk simpan otomatis, MoneyClip butuh Apps Script Web App endpoint.`

Jika Hermes punya kemampuan membuat Apps Script otomatis, buat endpoint dan simpan sebagai `moneyclip.sheet_url`.

Jika tidak, pandu user membuat endpoint atau minta user memasukkan endpoint manual.

### Langkah 4 — selesai setup

Setup dianggap selesai jika minimal salah satu ini benar:

- `moneyclip.sheet_url` sudah ada dan bisa menerima action MoneyClip.
- Hermes Agent punya akses langsung untuk membaca/menulis Google Sheet dari `moneyclip.sheet_link`.

Jika selesai, set `moneyclip.setup_complete` menjadi `true` jika Hermes mendukung penyimpanan config.

---

## Format sheet yang harus dibuat

Sheet `Pengeluaran`:

`ID | Timestamp | Tanggal | Jam | ChatID | MessageID | Deskripsi | Nominal | Kategori`

Sheet `Saldo`:

`Tanggal | ChatID | Saldo Awal | Total Keluar | Sisa`

Sheet `State`:

`ChatID | LastMessageID | LastDesc | LastAmount | LastTimestamp | LastEntryID`

---

## Input runtime

Runtime menerima payload berisi `chat_id`, `message_id`, `text`, dan `timestamp`.

Field wajib:
- `chat_id`
- `text`

Jika `timestamp` kosong, gunakan waktu saat ini berdasarkan `moneyclip.timezone`.

---

## Intent aktif setelah setup selesai

### Set saldo

Aktif untuk pesan seperti:
- `saldo 200rb`
- `saldo awal 500rb`
- `pegang 150rb`
- `ada uang 1jt`
- `cash 300rb`

Action: `set_balance`.

Balasan:

`💰 Saldo: Rp200.000. Siap!`

### Catat pengeluaran

Aktif jika ada aktivitas dan nominal, misalnya:
- `makan 25rb`
- `kopi 18k`
- `bensin 50rb`
- `parkir 5000`
- `kemarin beli obat 30rb`

Action: `add`.

Balasan satu transaksi:

`✅ makan Rp25.000`
`💰 Sisa: Rp175.000`

### Cek saldo

Aktif untuk:
- `sisa berapa`
- `saldo tinggal berapa`
- `cek saldo`
- `uangku berapa`

Action: `get_balance`.

Balasan:

`💰 Sisa: Rp125.000`
`📉 Keluar: Rp75.000 dari Rp200.000`

### Rekap

Aktif untuk:
- `rekap`
- `rekap hari ini`
- `rekap minggu ini`
- `rekap bulan ini`

Action: `recap` dengan period `today`, `week`, atau `month`.

Balasan:

`📊 Hari ini — 4 transaksi`
`📉 Keluar Rp82.000 | 💰 Sisa Rp118.000`

### Edit dan hapus

Edit aktif untuk:
- `edit makan jadi 20rb`
- `ubah yang tadi jadi 15rb`
- `transaksi terakhir 50rb`

Hapus aktif untuk:
- `hapus yang tadi`
- `hapus transaksi terakhir`
- `batal catat makan`

---

## Jangan catat

Jangan catat jika:
- Tidak ada nominal.
- User hanya bertanya harga.
- User hanya menyebut rencana beli.
- User bilang batal.
- User bilang ditraktir/dibayarin.
- User bilang nitip/ditalangin.

Balasan:

`Belum ada yang dicatat.`

---

## Parsing nominal

- `rb`, `ribu`, `k` dikali 1000.
- `jt`, `juta` dikali 1000000.
- Angka dengan titik atau koma dibaca sebagai rupiah langsung.
- Angka 6 digit atau lebih dibaca apa adanya.
- Aktivitas harian dengan angka kecil diasumsikan ribu.

Contoh:
- `25rb` → 25000
- `25k` → 25000
- `1jt` → 1000000
- `makan 25` → 25000
- `parkir 5` → 5000

Jika ambigu, tanya:

`Nominalnya berapa? pakai rb/jt ya.`

---

## Tanggal

Default pakai hari ini berdasarkan `moneyclip.timezone`.

Tanggal mundur:
- `kemarin` → H-1
- `2 hari lalu` → H-2
- `3 hari lalu` → H-3
- `tadi lupa` atau `lupa catat` → gunakan tanggal yang dimaksud jika jelas, kalau tidak hari ini.

Format tanggal action: `YYYY-MM-DD`.

---

## Kategori

- Makanan & Minuman: makan, nasi, kopi, minum, jajan, snack.
- Transport: bensin, parkir, tol, gojek, grab, angkot, bus, kereta.
- Tagihan & Utilitas: listrik, air, pulsa, paket data, wifi, token.
- Kesehatan: obat, dokter, klinik, apotek, vitamin.
- Hiburan & Langganan: nonton, bioskop, spotify, netflix, game.
- Pendidikan: buku, sekolah, kuliah, kelas, kursus.
- Belanja: baju, sepatu, skincare, barang, toko.
- Lainnya: selain kategori di atas.

---

## Logic khusus

Patungan: jika ada `patungan`, `berdua`, `bertiga`, `berempat`, atau `dibagi X`, catat hanya porsi user. Contoh `patungan makan 90rb bertiga` dicatat 30000.

Cicilan: jika ada kata `cicilan`, tambahkan `(cicilan)` pada deskripsi.

Transfer: jika ada kata `transfer`, jangan langsung catat. Tanya:

`Transfer untuk apa? Mau dicatat sebagai pengeluaran?`

Duplikasi: jika pesan sama atau mirip dengan transaksi terakhir kurang dari 1 menit, tanya:

`Lanjutan tadi atau transaksi baru?`

---

## Action contract jika memakai endpoint

Jika `moneyclip.sheet_url` tersedia, kirim HTTP POST ke endpoint tersebut.

Semua request harus membawa token jika `moneyclip.secret_token` tersedia.

Set saldo payload:
- action: `set_balance`
- chat_id
- amount
- date

Catat pengeluaran payload:
- action: `add`
- chat_id
- message_id
- date
- entries: desc, amount, category

Cek saldo payload:
- action: `get_balance`
- chat_id

Rekap payload:
- action: `recap`
- chat_id
- period

Edit payload:
- action: `edit`
- chat_id
- entry_id
- new_amount

Hapus payload:
- action: `delete`
- chat_id
- entry_id

---

## Action contract jika memakai akses langsung Google Sheet

Jika Hermes Agent punya tool untuk mengedit Google Sheet langsung, boleh tulis langsung ke tab:
- `Pengeluaran` untuk transaksi.
- `Saldo` untuk saldo awal, total keluar, dan sisa.
- `State` untuk transaksi terakhir dan deteksi duplikasi.

Setelah menulis, tetap balas dengan format MoneyClip.

---

## Error handling

Jika belum setup:

`Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.`

Jika akses Sheet ditolak:

`Belum bisa edit Sheet. Ubah akses ke Anyone with the link → Editor, lalu kirim ulang linknya.`

Jika saldo belum diset:

`Pegang uang berapa hari ini?`

Jika endpoint/token invalid:

`Akses MoneyClip belum valid.`

Jika timeout, retry sekali. Jika tetap gagal:

`Gagal simpan. Coba kirim ulang ya.`
