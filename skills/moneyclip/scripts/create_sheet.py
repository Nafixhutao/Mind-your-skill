#!/usr/bin/env python3
"""Create and prepare a MoneyClip Google Sheet.

Requires prior Google OAuth authorization through google_auth.py.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

DEFAULT_TOKEN = Path.home() / ".moneyclip" / "token.json"

SHEET_HEADERS = {
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


def get_services(token_path: Path):
    if not token_path.exists():
        raise FileNotFoundError(
            f"Missing token file: {token_path}. Run google_auth.py first."
        )
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    sheets = build("sheets", "v4", credentials=creds)
    return sheets


def create_spreadsheet(sheets, title: str) -> str:
    body = {
        "properties": {"title": title},
        "sheets": [
            {"properties": {"title": "Pengeluaran"}},
            {"properties": {"title": "Saldo"}},
            {"properties": {"title": "State"}},
        ],
    }
    result = sheets.spreadsheets().create(body=body).execute()
    return result["spreadsheetId"]


def write_headers(sheets, spreadsheet_id: str) -> None:
    data = []
    for sheet_name, headers in SHEET_HEADERS.items():
        data.append({
            "range": f"{sheet_name}!A1:{chr(ord('A') + len(headers) - 1)}1",
            "values": [headers],
        })
    sheets.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"valueInputOption": "RAW", "data": data},
    ).execute()


def freeze_headers(sheets, spreadsheet_id: str) -> None:
    meta = sheets.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    requests = []
    for sheet in meta.get("sheets", []):
        sheet_id = sheet["properties"]["sheetId"]
        requests.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {"frozenRowCount": 1},
                },
                "fields": "gridProperties.frozenRowCount",
            }
        })
    if requests:
        sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests},
        ).execute()


def main() -> None:
    parser = argparse.ArgumentParser(description="Create MoneyClip Google Sheet")
    parser.add_argument("--token", default=str(DEFAULT_TOKEN))
    parser.add_argument("--title", default="MoneyClip")
    args = parser.parse_args()

    token_path = Path(args.token).expanduser().resolve()
    sheets = get_services(token_path)
    spreadsheet_id = create_spreadsheet(sheets, args.title)
    write_headers(sheets, spreadsheet_id)
    freeze_headers(sheets, spreadsheet_id)

    print(json.dumps({
        "ok": True,
        "spreadsheet_id": spreadsheet_id,
        "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit",
        "message": "MoneyClip sheet created and configured.",
    }, indent=2))


if __name__ == "__main__":
    main()
