"""SQLite database helper functions."""

import sqlite3
from pathlib import Path
from typing import Any

from flask import g

from config import DATABASE_PATH


def get_db() -> sqlite3.Connection:
    """Return a database connection for the current Flask request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error: Exception | None = None) -> None:
    """Close the database connection at the end of a Flask request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def execute_query(query: str, params: tuple[Any, ...] = ()) -> sqlite3.Cursor:
    """Execute INSERT, UPDATE, or DELETE SQL and commit the transaction."""
    db = get_db()
    cursor = db.execute(query, params)
    db.commit()
    return cursor


def fetch_one(query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
    """Fetch one row from the database."""
    return get_db().execute(query, params).fetchone()


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
    """Fetch multiple rows from the database."""
    return list(get_db().execute(query, params).fetchall())


def database_exists() -> bool:
    """Return True when the SQLite database file exists."""
    return Path(DATABASE_PATH).exists()
