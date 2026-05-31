#!/usr/bin/env python3
"""Authorize MoneyClip for Google Sheets API.

This script performs a local OAuth flow and stores the user token outside the
repository by default. Do not commit client_secret.json or token.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

DEFAULT_DIR = Path.home() / ".moneyclip"
DEFAULT_CLIENT_SECRET = DEFAULT_DIR / "client_secret.json"
DEFAULT_TOKEN = DEFAULT_DIR / "token.json"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_credentials(token_path: Path, scopes: Iterable[str]) -> Credentials | None:
    if not token_path.exists():
        return None
    creds = Credentials.from_authorized_user_file(str(token_path), list(scopes))
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds if creds and creds.valid else None


def authorize(client_secret_path: Path, token_path: Path) -> Credentials:
    if not client_secret_path.exists():
        raise FileNotFoundError(
            f"Missing OAuth client file: {client_secret_path}\n"
            "Create an OAuth Desktop Client in Google Cloud, download it as "
            "client_secret.json, and place it there."
        )

    ensure_dir(token_path.parent)
    existing = load_credentials(token_path, SCOPES)
    if existing:
        return existing

    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
    creds = flow.run_local_server(port=0)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def main() -> None:
    parser = argparse.ArgumentParser(description="Authorize MoneyClip Google access")
    parser.add_argument("--client-secret", default=str(DEFAULT_CLIENT_SECRET))
    parser.add_argument("--token", default=str(DEFAULT_TOKEN))
    args = parser.parse_args()

    client_secret_path = Path(args.client_secret).expanduser().resolve()
    token_path = Path(args.token).expanduser().resolve()
    creds = authorize(client_secret_path, token_path)

    print(json.dumps({
        "ok": True,
        "token_path": str(token_path),
        "scopes": creds.scopes,
        "message": "MoneyClip Google authorization is ready.",
    }, indent=2))


if __name__ == "__main__":
    main()
