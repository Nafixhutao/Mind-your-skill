#!/usr/bin/env python3
"""MoneyClip Google Sheets operations helper.

This helper lets Hermes write MoneyClip actions through the official Google
Sheets API after the user authorizes Google once with google_auth.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

DEFAULT_TOKEN = Path.home() / ".moneyclip" / "token.json"
TZ = ZoneInfo("Asia/Jakarta")

HEADERS = {
    "Pengeluaran": [
        "ID",
        "Timestamp",
        "Tanggal",
        "Jam",
        "ChatID",
        "MessageID",
        "Deskripsi",
        "Nominal",
        "Kategori",
    ],
    "Saldo": [
        "Tanggal",
        "ChatID",
        "Saldo Awal",
        "Total Keluar",
        "Sisa",
    ],
    "State": [
        "ChatID",
        "LastMessageID",
        "LastDesc",
        "LastAmount",
        "LastTimestamp",
        "LastEntryID",
    ],
}


def service(token_path: Path):
    if not token_path.exists():
        raise FileNotFoundError(f"Missing token file: {token_path}. Run google_auth.py first.")
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    return build("sheets", "v4", credentials=creds)


def values_api(sheets):
    return sheets.spreadsheets().values()


def get_values(sheets, spreadsheet_id: str, range_name: str):
    result = values_api(sheets).get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get("values", [])


def update_values(sheets, spreadsheet_id: str, range_name: str, values):
    values_api(sheets).update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body={"values": values},
    ).execute()


def append_values(sheets, spreadsheet_id: str, range_name: str, values):
    values_api(sheets).append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": values},
    ).execute()


def ensure_headers(sheets, spreadsheet_id: str):
    data = []
    for sheet_name, headers in HEADERS.items():
        end_col = chr(ord("A") + len(headers) - 1)
        data.append({"range": f"{sheet_name}!A1:{end_col}1", "values": [headers]})
    sheets.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"valueInputOption": "RAW", "data": data},
    ).execute()


def now_parts():
    now = datetime.now(TZ)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
    }


def to_int(value) -> int:
    try:
        return int(round(float(value or 0)))
    except Exception:
        return 0


def find_balance_row(rows, chat_id: str):
    for index, row in enumerate(rows[1:], start=2):
        if len(row) > 1 and str(row[1]) == str(chat_id):
            return index, row
    return None, None


def get_balance(sheets, spreadsheet_id: str, chat_id: str):
    rows = get_values(sheets, spreadsheet_id, "Saldo!A:E")
    row_index, row = find_balance_row(rows, chat_id)
    if not row:
        return {"row": None, "starting_balance": 0, "total_spent": 0, "remaining_balance": 0}
    return {
        "row": row_index,
        "starting_balance": to_int(row[2] if len(row) > 2 else 0),
        "total_spent": to_int(row[3] if len(row) > 3 else 0),
        "remaining_balance": to_int(row[4] if len(row) > 4 else 0),
    }


def set_balance(sheets, spreadsheet_id: str, chat_id: str, amount: int):
    ensure_headers(sheets, spreadsheet_id)
    rows = get_values(sheets, spreadsheet_id, "Saldo!A:E")
    row_index, _ = find_balance_row(rows, chat_id)
    parts = now_parts()
    row = [[parts["date"], chat_id, amount, 0, amount]]
    if row_index:
        update_values(sheets, spreadsheet_id, f"Saldo!A{row_index}:E{row_index}", row)
    else:
        append_values(sheets, spreadsheet_id, "Saldo!A:E", row)
    return {"ok": True, "action": "set_balance", "remaining_balance": amount}


def upsert_state(sheets, spreadsheet_id: str, chat_id: str, message_id: str, desc: str, amount: int, timestamp: str, entry_id: str):
    rows = get_values(sheets, spreadsheet_id, "State!A:F")
    target = [[chat_id, message_id, desc, amount, timestamp, entry_id]]
    for index, row in enumerate(rows[1:], start=2):
        if row and str(row[0]) == str(chat_id):
            update_values(sheets, spreadsheet_id, f"State!A{index}:F{index}", target)
            return
    append_values(sheets, spreadsheet_id, "State!A:F", target)


def add_expense(sheets, spreadsheet_id: str, chat_id: str, message_id: str, entries):
    ensure_headers(sheets, spreadsheet_id)
    balance = get_balance(sheets, spreadsheet_id, chat_id)
    if balance["row"] is None:
        raise RuntimeError("BALANCE_MISSING")

    parts = now_parts()
    rows = []
    total = 0
    last_entry_id = ""
    for entry in entries:
        amount = to_int(entry.get("amount"))
        desc = str(entry.get("desc") or entry.get("description") or "Pengeluaran")
        category = str(entry.get("category") or "Lainnya")
        entry_id = "EXP-" + uuid.uuid4().hex[:12]
        rows.append([
            entry_id,
            parts["timestamp"],
            entry.get("date") or parts["date"],
            parts["time"],
            chat_id,
            message_id,
            desc,
            amount,
            category,
        ])
        total += amount
        last_entry_id = entry_id
        upsert_state(sheets, spreadsheet_id, chat_id, message_id, desc, amount, parts["timestamp"], entry_id)

    append_values(sheets, spreadsheet_id, "Pengeluaran!A:I", rows)
    new_spent = balance["total_spent"] + total
    new_remaining = balance["starting_balance"] - new_spent
    update_values(
        sheets,
        spreadsheet_id,
        f"Saldo!A{balance['row']}:E{balance['row']}",
        [[parts["date"], chat_id, balance["starting_balance"], new_spent, new_remaining]],
    )
    return {
        "ok": True,
        "action": "add",
        "total_added": total,
        "remaining_balance": new_remaining,
        "last_entry_id": last_entry_id,
    }


def recap_today(sheets, spreadsheet_id: str, chat_id: str):
    rows = get_values(sheets, spreadsheet_id, "Pengeluaran!A:I")
    today = now_parts()["date"]
    total = 0
    count = 0
    categories = {}
    largest = None
    for row in rows[1:]:
        if len(row) < 9:
            continue
        if str(row[4]) != str(chat_id):
            continue
        if str(row[2]) != today:
            continue
        amount = to_int(row[7])
        category = row[8] or "Lainnya"
        desc = row[6] or "Pengeluaran"
        total += amount
        count += 1
        categories[category] = categories.get(category, 0) + amount
        if not largest or amount > largest["amount"]:
            largest = {"desc": desc, "amount": amount, "category": category}
    return {
        "ok": True,
        "action": "recap",
        "period": "today",
        "transaction_count": count,
        "total_spent": total,
        "categories": categories,
        "largest": largest,
        "balance": get_balance(sheets, spreadsheet_id, chat_id),
    }


def run_action(payload: dict, token_path: Path):
    sheets = service(token_path)
    spreadsheet_id = payload.get("spreadsheet_id")
    if not spreadsheet_id:
        raise RuntimeError("MISSING_SPREADSHEET_ID")
    action = payload.get("action")
    chat_id = str(payload.get("chat_id") or "default")
    message_id = str(payload.get("message_id") or "")

    if action == "setup":
        ensure_headers(sheets, spreadsheet_id)
        return {"ok": True, "action": "setup", "spreadsheet_id": spreadsheet_id}
    if action == "set_balance":
        return set_balance(sheets, spreadsheet_id, chat_id, to_int(payload.get("amount")))
    if action == "add":
        entries = payload.get("entries") or []
        if not isinstance(entries, list) or not entries:
            raise RuntimeError("NO_ENTRIES")
        return add_expense(sheets, spreadsheet_id, chat_id, message_id, entries)
    if action == "get_balance":
        result = get_balance(sheets, spreadsheet_id, chat_id)
        result.update({"ok": True, "action": "get_balance"})
        return result
    if action == "recap":
        return recap_today(sheets, spreadsheet_id, chat_id)
    raise RuntimeError(f"UNKNOWN_ACTION: {action}")


def main():
    parser = argparse.ArgumentParser(description="Run MoneyClip Google Sheets action")
    parser.add_argument("--token", default=str(DEFAULT_TOKEN))
    parser.add_argument("--payload", help="JSON payload string. If omitted, stdin is used.")
    args = parser.parse_args()
    raw = args.payload if args.payload else sys.stdin.read()
    payload = json.loads(raw)
    result = run_action(payload, Path(args.token).expanduser().resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
