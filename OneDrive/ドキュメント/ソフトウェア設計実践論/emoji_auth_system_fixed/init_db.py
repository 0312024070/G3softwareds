"""Initialize the SQLite database for the authentication system."""

import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash

from config import DATABASE_PATH


SCHEMA_SQL = """
DROP TABLE IF EXISTS login_logs;
DROP TABLE IF EXISTS emoji_codes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE,
    role_description TEXT NOT NULL
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    mail_address TEXT NOT NULL,
    phone_number TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles (role_id)
);

CREATE TABLE emoji_codes (
    code_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    symbol_order TEXT NOT NULL,
    expiration_time TEXT NOT NULL,
    used_flag INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE login_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    login_time TEXT NOT NULL,
    result TEXT NOT NULL,
    access_ip TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
"""


def insert_seed_data(connection: sqlite3.Connection) -> None:
    """Insert roles and sample users."""
    now = datetime.now().isoformat(timespec="seconds")

    connection.executemany(
        "INSERT INTO roles (role_name, role_description) VALUES (?, ?)",
        [
            ("user", "一般利用者"),
            ("admin", "管理者"),
        ],
    )

    role_rows = connection.execute("SELECT role_id, role_name FROM roles").fetchall()
    role_map = {row["role_name"]: row["role_id"] for row in role_rows}

    users = [
        (
            "murata_taro",
            "村田 太郎",
            generate_password_hash("password123"),
            role_map["user"],
            "murata_taro@example.com",
            "090-0000-0001",
            1,
            now,
        ),
        (
            "admin",
            "山田 太郎",
            generate_password_hash("admin123"),
            role_map["admin"],
            "admin@example.com",
            "090-0000-0002",
            1,
            now,
        ),
        (
            "tanaka_ken",
            "田中 健二",
            generate_password_hash("password123"),
            role_map["user"],
            "tanaka_ken@example.com",
            "090-0000-0003",
            1,
            now,
        ),
    ]

    connection.executemany(
        """
        INSERT INTO users
            (user_id, name, password_hash, role_id, mail_address,
             phone_number, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        users,
    )


def initialize_database() -> None:
    """Create the database schema and seed data."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    with connection:
        connection.executescript(SCHEMA_SQL)
        insert_seed_data(connection)

    connection.close()
    print(f"Database initialized: {DATABASE_PATH}")


if __name__ == "__main__":
    initialize_database()
