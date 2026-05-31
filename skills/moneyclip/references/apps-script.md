# MoneyClip Apps Script

Use this reference to create or verify the Apps Script code included in the MoneyClip Google Sheet template.

This script acts as a Web App endpoint. Hermes sends MoneyClip actions to the Web App URL, and the script writes to the copied Google Sheet.

## Required deployment settings

```text
Deploy → New deployment → Web app
Execute as: Me
Who has access: Anyone
```

## Code

```javascript
const TZ = "Asia/Jakarta";

const SHEETS = {
  EXPENSES: "Pengeluaran",
  BALANCE: "Saldo",
  STATE: "State",
};

const HEADERS = {
  Pengeluaran: ["ID", "Timestamp", "Tanggal", "Jam", "ChatID", "MessageID", "Deskripsi", "Nominal", "Kategori"],
  Saldo: ["Tanggal", "ChatID", "Saldo Awal", "Total Keluar", "Sisa"],
  State: ["ChatID", "LastMessageID", "LastDesc", "LastAmount", "LastTimestamp", "LastEntryID"],
};

function doGet(e) {
  setupMoneyClip();
  return json({ ok: true, service: "MoneyClip", message: "MoneyClip endpoint aktif." });
}

function doPost(e) {
  try {
    setupMoneyClip();
    const body = e && e.postData && e.postData.contents ? JSON.parse(e.postData.contents) : {};
    const action = body.action;

    if (action === "ping") return json({ ok: true, message: "pong" });
    if (action === "setup") return json({ ok: true, message: "setup_complete" });

    if (action === "set_balance") {
      const chatId = String(body.chat_id || "default");
      const amount = toInt(body.amount);
      setBalance(chatId, amount);
      return json({ ok: true, action: "set_balance", balance: amount, remaining_balance: amount });
    }

    if (action === "add") {
      const chatId = String(body.chat_id || "default");
      const messageId = String(body.message_id || "");
      const entries = Array.isArray(body.entries) ? body.entries : [];
      if (!entries.length) throw new Error("NO_ENTRIES");
      const result = addExpenses(chatId, messageId, entries);
      return json({ ok: true, action: "add", total_added: result.totalAdded, remaining_balance: result.remaining });
    }

    if (action === "get_balance") {
      const chatId = String(body.chat_id || "default");
      const balance = getBalance(chatId);
      return json({ ok: true, action: "get_balance", starting_balance: balance.starting, total_spent: balance.spent, remaining_balance: balance.remaining });
    }

    if (action === "recap") {
      const chatId = String(body.chat_id || "default");
      const period = String(body.period || "today");
      return json({ ok: true, action: "recap", period, recap: recap(chatId, period), balance: getBalance(chatId) });
    }

    throw new Error("UNKNOWN_ACTION: " + action);
  } catch (err) {
    return json({ ok: false, error: String(err.message || err) });
  }
}

function setupMoneyClip() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  Object.keys(HEADERS).forEach((sheetName) => {
    let sheet = ss.getSheetByName(sheetName);
    if (!sheet) sheet = ss.insertSheet(sheetName);
    const headers = HEADERS[sheetName];
    const current = sheet.getRange(1, 1, 1, headers.length).getValues()[0];
    const needsHeader = headers.some((h, i) => current[i] !== h);
    if (needsHeader) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.setFrozenRows(1);
      sheet.autoResizeColumns(1, headers.length);
    }
  });
}

function setBalance(chatId, amount) {
  const sheet = getSheet(SHEETS.BALANCE);
  const row = findBalanceRow(chatId);
  const today = formatDate(new Date());
  const values = [[today, chatId, amount, 0, amount]];
  if (row) sheet.getRange(row, 1, 1, 5).setValues(values);
  else sheet.appendRow(values[0]);
}

function addExpenses(chatId, messageId, entries) {
  const expenseSheet = getSheet(SHEETS.EXPENSES);
  const balance = getBalance(chatId);
  if (balance.row === null) throw new Error("BALANCE_MISSING");

  const now = new Date();
  const timestamp = now.toISOString();
  const tanggal = formatDate(now);
  const jam = Utilities.formatDate(now, TZ, "HH:mm:ss");
  let totalAdded = 0;
  let lastEntryId = "";

  entries.forEach((entry) => {
    const amount = toInt(entry.amount);
    const desc = String(entry.desc || entry.description || "Pengeluaran");
    const category = String(entry.category || "Lainnya");
    const id = "EXP-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
    expenseSheet.appendRow([id, timestamp, entry.date || tanggal, jam, chatId, messageId, desc, amount, category]);
    totalAdded += amount;
    lastEntryId = id;
    upsertState(chatId, messageId, desc, amount, timestamp, id);
  });

  const newSpent = balance.spent + totalAdded;
  const newRemaining = balance.starting - newSpent;
  getSheet(SHEETS.BALANCE).getRange(balance.row, 1, 1, 5).setValues([[tanggal, chatId, balance.starting, newSpent, newRemaining]]);

  return { totalAdded, remaining: newRemaining, lastEntryId };
}

function getBalance(chatId) {
  const sheet = getSheet(SHEETS.BALANCE);
  const values = sheet.getDataRange().getValues();
  for (let i = 1; i < values.length; i++) {
    if (String(values[i][1]) === String(chatId)) {
      return { row: i + 1, starting: toInt(values[i][2]), spent: toInt(values[i][3]), remaining: toInt(values[i][4]) };
    }
  }
  return { row: null, starting: 0, spent: 0, remaining: 0 };
}

function findBalanceRow(chatId) {
  const values = getSheet(SHEETS.BALANCE).getDataRange().getValues();
  for (let i = 1; i < values.length; i++) {
    if (String(values[i][1]) === String(chatId)) return i + 1;
  }
  return null;
}

function upsertState(chatId, messageId, desc, amount, timestamp, entryId) {
  const sheet = getSheet(SHEETS.STATE);
  const values = sheet.getDataRange().getValues();
  const row = [[chatId, messageId, desc, amount, timestamp, entryId]];
  for (let i = 1; i < values.length; i++) {
    if (String(values[i][0]) === String(chatId)) {
      sheet.getRange(i + 1, 1, 1, 6).setValues(row);
      return;
    }
  }
  sheet.appendRow(row[0]);
}

function recap(chatId, period) {
  const values = getSheet(SHEETS.EXPENSES).getDataRange().getValues();
  const today = formatDate(new Date());
  const categories = {};
  let total = 0;
  let count = 0;
  let largest = null;

  for (let i = 1; i < values.length; i++) {
    const rowChatId = String(values[i][4]);
    const tanggal = String(values[i][2]);
    const desc = String(values[i][6]);
    const amount = toInt(values[i][7]);
    const category = String(values[i][8] || "Lainnya");
    if (rowChatId !== String(chatId)) continue;
    if (period === "today" && tanggal !== today) continue;
    total += amount;
    count += 1;
    categories[category] = (categories[category] || 0) + amount;
    if (!largest || amount > largest.amount) largest = { desc, amount, category };
  }

  return { transaction_count: count, total_spent: total, categories, largest };
}

function getSheet(name) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
  if (!sheet) throw new Error("MISSING_SHEET: " + name);
  return sheet;
}

function formatDate(date) {
  return Utilities.formatDate(date, TZ, "yyyy-MM-dd");
}

function toInt(value) {
  const n = Number(value || 0);
  if (!Number.isFinite(n)) return 0;
  return Math.round(n);
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
```
