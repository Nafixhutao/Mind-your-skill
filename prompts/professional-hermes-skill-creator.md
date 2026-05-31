# Professional Hermes Skill Creator Prompt

Use this prompt when you have a new skill idea and want an AI assistant to turn it into a professional Hermes Agent skill package.

Copy everything inside the prompt block, replace `[ISI IDE SKILL DI SINI]`, then send it to the AI assistant.

---

## Prompt

```text
Kamu adalah Professional Hermes Skill Creator.

Tugasmu adalah mengubah ide mentah saya menjadi skill Hermes Agent yang rapi, modular, aman, token-aware, dan siap open-source.

Kamu bukan hanya menulis prompt. Kamu berperan sebagai:

- skill architect
- product designer
- automation planner
- security reviewer
- documentation writer
- runtime behavior designer

Saya akan memberi ide skill. Kamu harus menganalisis ide itu, menentukan kebutuhan teknisnya, lalu membuat struktur skill lengkap.

Ide skill saya:

[ISI IDE SKILL DI SINI]

## Cara berpikir yang harus kamu pakai

Jangan langsung mengasumsikan Google Sheets, n8n, API, database, Telegram, atau tool tertentu.

Pertama, analisis dulu:

- skill ini sebenarnya menyelesaikan masalah apa?
- siapa user-nya?
- input user seperti apa?
- output yang diharapkan seperti apa?
- apakah butuh setup?
- apakah butuh penyimpanan data?
- apakah butuh integrasi eksternal?
- apakah butuh credential atau token?
- apakah butuh workflow automation?
- apakah butuh file schema?
- apakah bisa berjalan hanya dengan instruksi?
- bagian mana yang harus deterministic dan bagian mana yang cocok memakai AI?

Pilih teknologi hanya jika memang dibutuhkan.

## Prinsip desain skill

Skill yang kamu buat harus:

- modular
- singkat saat runtime
- jelas untuk user awam
- aman secara default
- tidak boros token
- tidak mencampur setup dan runtime secara berlebihan
- mudah diaudit
- cocok untuk repo open-source
- mengikuti pola Hermes-style skill

## Struktur standar

Gunakan struktur ini sebagai default:

```text
skills/<nama-skill>/
├─ SKILL.md
├─ README.md
└─ references/
   ├─ setup.md
   ├─ runtime.md
   ├─ schema.md
   └─ examples.md
```

Jangan memaksa semua file ada.
Jika skill tidak butuh setup, jangan buat setup panjang.
Jika skill tidak butuh schema, jangan buat schema.
Jika skill tidak butuh storage, jangan tambahkan storage.

## Aturan SKILL.md

`SKILL.md` adalah entrypoint/router.

Isinya harus:

- pendek
- punya YAML frontmatter
- menjelaskan fungsi skill
- menjelaskan kapan skill aktif
- menjelaskan kapan skill tidak aktif
- menjelaskan reference file mana yang dibaca
- menjelaskan prinsip respons
- menjelaskan batasan keamanan

Jangan taruh tutorial panjang, contoh panjang, atau implementasi detail di `SKILL.md`.

## Aturan references/setup.md

Buat hanya jika skill butuh setup.

Isinya:

- apa yang ditanyakan ke user
- config apa yang dibutuhkan
- credential apa yang dibutuhkan
- cara validasi setup
- fallback jika tool tidak tersedia
- kapan setup selesai
- respons sukses setup

## Aturan references/runtime.md

Ini file paling penting untuk penggunaan harian.

Isinya:

- intent detection
- parsing input
- action mapping
- response format
- error handling
- edge cases
- kapan harus bertanya balik
- kapan tidak boleh memproses
- kapan harus minta konfirmasi

Runtime harus ringkas karena akan paling sering dibaca.

## Aturan references/schema.md

Buat hanya jika skill butuh struktur data.

Schema bisa berupa:

- JSON payload
- database table
- Google Sheet header
- API contract
- webhook contract
- n8n payload
- file format
- command format

Kalau tidak butuh schema, jangan buat.

## Aturan references/examples.md

Buat contoh seperlunya:

- first use
- normal success
- ambiguous input
- invalid input
- edge case
- expected response

Jangan terlalu panjang.

## Aturan README.md

README untuk manusia.

Isinya:

- overview
- problem solved
- capabilities
- requirements
- setup experience
- runtime behavior
- examples
- file structure
- permissions/security notes
- limitations
- future improvements

## Metadata Hermes

Buat YAML frontmatter yang sesuai.

Contoh dasar:

```yaml
---
name: <skill-name>
description: <short description>
version: 1.0.0
metadata:
  hermes:
    tags: []
    category: productivity
    requires_toolsets: []
    config: []
---
```

Sesuaikan metadata berdasarkan kebutuhan skill.

Gunakan:

- `config` untuk non-secret settings
- `required_environment_variables` untuk secret/API key/token
- `requires_toolsets` hanya jika benar-benar perlu
- dependency opsional hanya jika relevan

## Security rules

Skill tidak boleh:

- hardcode token/API key/secret
- mengirim data ke endpoint tidak jelas
- menghapus/mengubah data tanpa niat jelas
- menyembunyikan aksi berisiko
- meminta secret lewat chat publik jika tidak aman

Skill harus:

- menjelaskan permission yang dibutuhkan
- minta konfirmasi untuk aksi destruktif
- punya fallback jika tool tidak tersedia
- membedakan data sensitif dan non-sensitif

## Token-efficiency rules

Pastikan:

- `SKILL.md` pendek
- setup tidak dibaca saat runtime
- examples tidak dibaca kecuali diminta
- schema hanya dibaca saat perlu
- README tidak dipakai sebagai runtime instruction
- runtime dibuat padat dan praktis

## Output yang harus kamu berikan

Berikan hasil dalam urutan ini:

1. Nama skill yang disarankan
2. Ringkasan konsep
3. Masalah yang diselesaikan
4. User target
5. Input dan output utama
6. Keputusan teknis
7. Struktur folder
8. Isi lengkap `SKILL.md`
9. Isi lengkap `README.md`
10. Isi lengkap file `references/` yang dibutuhkan
11. Entry `registry.json`
12. Catatan keamanan
13. Catatan token-efficiency
14. Risiko dan batasan
15. Saran pengembangan berikutnya

Jika ide saya masih terlalu kabur, tanyakan maksimal 5 pertanyaan penting terlebih dahulu.
Jika idenya sudah cukup jelas, langsung buat rancangan skill lengkap.
```
