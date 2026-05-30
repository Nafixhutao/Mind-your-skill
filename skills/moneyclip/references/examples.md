# MoneyClip Examples

Use examples only when the user asks what MoneyClip can do or needs guidance.

## First setup

User:

```text
pakai moneyclip
```

Assistant:

```text
Kirim link Google Sheet untuk MoneyClip ya. Pastikan aksesnya Editor.
```

User:

```text
https://docs.google.com/spreadsheets/d/...
```

Assistant:

```text
✅ Sheet MoneyClip siap.
Sekarang kirim: saldo 200rb
```

## Runtime

User:

```text
saldo 200rb
```

Assistant:

```text
💰 Saldo: Rp200.000. Siap!
```

User:

```text
makan 25rb
```

Assistant:

```text
✅ makan Rp25.000
💰 Sisa: Rp175.000
```

User:

```text
bensin 50rb
```

Assistant:

```text
✅ bensin Rp50.000
💰 Sisa: Rp125.000
```

User:

```text
kemarin beli obat 30rb
```

Assistant:

```text
✅ beli obat Rp30.000
💰 Sisa: Rp95.000
```

User:

```text
sisa berapa
```

Assistant:

```text
💰 Sisa: Rp95.000
📉 Keluar: Rp105.000 dari Rp200.000
```

## Ambiguous amount

User:

```text
beli laptop 5
```

Assistant:

```text
Nominalnya berapa? pakai rb/jt ya.
```

## Transfer

User:

```text
transfer 100rb
```

Assistant:

```text
Transfer untuk apa? Mau dicatat sebagai pengeluaran?
```

## Patungan

User:

```text
patungan makan 90rb bertiga
```

Assistant:

```text
✅ patungan makan Rp30.000
💰 Sisa: Rp170.000
```
