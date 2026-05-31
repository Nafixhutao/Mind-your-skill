# Personal Finance Ledger

`personal-finance-ledger` is a Hermes Agent skill for tracking personal income and expenses using natural language and receipt images.

It accepts free-text transaction input such as:

```text
beli kopi 15rb
gajian 5jt
bayar listrik 350000
```

It can also process receipt images when OCR tooling is available, extract the merchant and total amount, infer a category, and save the transaction to Google Sheets.

## Problem solved

Personal finance tracking is often abandoned because users must manually open a spreadsheet, remember the right columns, categorize transactions, and type every amount.

This skill reduces friction by letting users record transactions conversationally.

## Capabilities

- Record expenses from free text.
- Record income from free text.
- Read receipt images using OCR when available.
- Extract merchant name and total amount from receipts.
- Infer transaction category from description or merchant.
- Save transactions to Google Sheets.
- Summarize balance, income, and expenses.
- Summarize expenses by category.
- Handle ambiguous or incomplete input with short clarification questions.

## Requirements

Required:

- Google Sheets access.
- Google Service Account credentials.
- A target spreadsheet ID.
- A transaction sheet with the expected headers.

Optional:

- OCR toolset for receipt image processing.
- File input toolset for uploaded receipt images.

## Setup experience

The user or deployer must provide:

- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `FINANCE_SHEET_ID`
- optional sheet/config values such as currency and timezone

The target Google Sheet must be shared with the service account email.

The skill should validate setup by checking:

1. credentials are available,
2. the spreadsheet is accessible,
3. the transaction sheet exists,
4. required headers are present.

## Runtime behavior

The skill detects one of these intents:

- record expense
- record income
- record receipt expense
- show balance summary
- show category summary
- correct or update transaction
- setup check

For normal transaction recording, the skill should parse the transaction, infer missing fields when safe, append a row to Google Sheets, then return a short confirmation.

For receipt uploads, the skill should run OCR if available, extract the merchant and total, infer category, then save the transaction as an expense.

For summaries, the skill should read transactions from Google Sheets, filter by date range, aggregate data, and respond with a concise summary.

## Examples

```text
User: beli kopi 15rb
Assistant: Tercatat: pengeluaran Rp15.000 untuk Makanan & Minuman.
```

```text
User: gajian 5jt
Assistant: Tercatat: pemasukan Rp5.000.000 untuk Gaji.
```

```text
User: ringkasan bulan ini
Assistant:
Saldo bulan ini: Rp4.250.000
Pemasukan: Rp7.000.000
Pengeluaran: Rp2.750.000
Kategori terbesar: Makanan & Minuman — Rp850.000
```

## File structure

```text
skills/personal-finance-ledger/
├─ SKILL.md
├─ README.md
└─ references/
   ├─ setup.md
   ├─ runtime.md
   ├─ schema.md
   └─ examples.md
```

## Permissions and security notes

This skill requires access to a Google Sheet containing financial records. The Google Service Account should be granted the minimum permission required.

Recommended permission:

- Editor access only to the target spreadsheet.

Do not share access to the entire Google Drive unless absolutely necessary.

Secrets must be provided as environment variables, never hardcoded in skill files.

## Limitations

- OCR accuracy depends on image quality.
- Category inference may be wrong for vague descriptions.
- This skill is for personal record keeping, not accounting or tax advice.
- Multi-currency handling is basic unless extended.
- It does not automatically reconcile bank accounts.

## Future improvements

- Budget limits per category.
- Recurring transaction detection.
- Duplicate receipt detection.
- Monthly charts.
- Export to CSV.
- Multi-account support.
- Bank statement import.
- Transaction editing workflow.
