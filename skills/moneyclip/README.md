# MoneyClip

MoneyClip is a Hermes Agent skill for personal daily expense tracking.

It is designed for Indonesian daily chat patterns such as:

```text
saldo 200rb
makan 25rb
bensin 50rb
kemarin beli obat 30rb
sisa berapa
rekap hari ini
```

## Capabilities

- First-run setup wizard
- Google Sheet storage preparation
- Set starting cash balance
- Record daily expenses
- Infer categories
- Handle Indonesian nominal shorthand such as `rb`, `k`, `jt`
- Track remaining balance
- Support recap, edit, and delete flows

## Skill files

```text
skills/moneyclip/
├─ SKILL.md
├─ setup.md
├─ runtime.md
├─ sheets-schema.md
├─ examples.md
└─ README.md
```

`SKILL.md` is the entrypoint and router. It tells Hermes which supporting file to use.

## Setup experience

When a user starts MoneyClip for the first time, the skill should ask for a Google Sheet link:

```text
Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.
```

After the user provides the sheet, Hermes prepares the required tabs and headers.

## Storage

MoneyClip supports two storage modes:

1. Direct Google Sheet editing, if Hermes has the right tool and access.
2. HTTP endpoint mode using `moneyclip.sheet_url`, usually a Google Apps Script Web App.

## Required tabs

- `Pengeluaran`
- `Saldo`
- `State`

See `sheets-schema.md` for exact headers.

## Runtime behavior

After setup, normal user messages should stay short:

```text
✅ makan Rp25.000
💰 Sisa: Rp175.000
```

MoneyClip should not read setup instructions during normal daily tracking unless setup is incomplete.

## Security notes

- Do not hardcode secrets.
- Do not send data to unconfigured endpoints.
- Do not delete existing spreadsheet data during setup.
- Ask for user confirmation before destructive actions if the intent is unclear.
