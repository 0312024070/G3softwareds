"""Service for creating and verifying emoji one-time codes."""

import random
from datetime import datetime, timedelta

from config import CODE_EXPIRATION_MINUTES, EMOJI_CODE_LENGTH, EMOJI_SYMBOLS
from database import execute_query, fetch_one


class EmojiService:
    """Manage emoji authentication codes."""

    @staticmethod
    def create_code(user_id: str) -> dict[str, object]:
        """Create a one-time emoji code for the specified user."""
        symbols = random.sample(EMOJI_SYMBOLS, EMOJI_CODE_LENGTH)
        symbol_order = ",".join(symbols)
        expiration_time = datetime.now() + timedelta(minutes=CODE_EXPIRATION_MINUTES)

        cursor = execute_query(
            """
            INSERT INTO emoji_codes
                (user_id, symbol_order, expiration_time, used_flag)
            VALUES (?, ?, ?, 0)
            """,
            (user_id, symbol_order, expiration_time.isoformat(timespec="seconds")),
        )

        return {
            "code_id": cursor.lastrowid,
            "symbol_order": symbols,
            "expiration_time": expiration_time,
        }

    @staticmethod
    def get_code(code_id: int) -> dict[str, object] | None:
        """Return an emoji code by ID."""
        row = fetch_one(
            """
            SELECT code_id, user_id, symbol_order, expiration_time, used_flag
            FROM emoji_codes
            WHERE code_id = ?
            """,
            (code_id,),
        )
        if row is None:
            return None

        return {
            "code_id": row["code_id"],
            "user_id": row["user_id"],
            "symbol_order": row["symbol_order"].split(","),
            "expiration_time": datetime.fromisoformat(row["expiration_time"]),
            "used_flag": bool(row["used_flag"]),
        }

    @staticmethod
    def is_expired(code: dict[str, object]) -> bool:
        """Return True when the emoji code is expired."""
        expiration_time = code["expiration_time"]
        if not isinstance(expiration_time, datetime):
            return True
        return datetime.now() > expiration_time

    @staticmethod
    def verify_code(code_id: int, selected_symbols: list[str]) -> str:
        """Verify selected emojis.

        Returns:
            SUCCESS: selected symbols are correct.
            EXPIRED: code has expired.
            USED: code has already been used.
            FAILED: selected symbols are incorrect.
        """
        code = EmojiService.get_code(code_id)
        if code is None:
            return "FAILED"

        if bool(code["used_flag"]):
            return "USED"

        if EmojiService.is_expired(code):
            return "EXPIRED"

        if selected_symbols == code["symbol_order"]:
            execute_query(
                "UPDATE emoji_codes SET used_flag = 1 WHERE code_id = ?",
                (code_id,),
            )
            return "SUCCESS"

        return "FAILED"

    @staticmethod
    def get_shuffled_symbols() -> list[str]:
        """Return emojis in a random order for the authentication screen."""
        symbols = EMOJI_SYMBOLS.copy()
        random.shuffle(symbols)
        return symbols
