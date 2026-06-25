"""Authentication service."""

from werkzeug.security import check_password_hash

from database import fetch_all, fetch_one
from services.emoji_service import EmojiService
from services.notification_service import NotificationService


class AuthService:
    """Control password authentication and emoji authentication."""

    @staticmethod
    def find_user(user_id: str) -> dict[str, object] | None:
        """Return a user by ID."""
        row = fetch_one(
            """
            SELECT
                u.user_id,
                u.name,
                u.password_hash,
                u.role_id,
                r.role_name,
                u.mail_address,
                u.phone_number,
                u.is_active
            FROM users AS u
            JOIN roles AS r ON u.role_id = r.role_id
            WHERE u.user_id = ?
            """,
            (user_id,),
        )
        if row is None:
            return None
        return dict(row)

    @staticmethod
    def verify_password(user_id: str, password: str) -> dict[str, object] | None:
        """Verify user ID and password."""
        user = AuthService.find_user(user_id)
        if user is None:
            return None

        if not bool(user["is_active"]):
            return None

        if not check_password_hash(str(user["password_hash"]), password):
            return None

        return user

    @staticmethod
    def start_emoji_auth(user: dict[str, object]) -> dict[str, object]:
        """Create an emoji code and send notification."""
        code = EmojiService.create_code(str(user["user_id"]))
        NotificationService.send_emoji_code(
            str(user["mail_address"]),
            list(code["symbol_order"]),
        )
        return code

    @staticmethod
    def check_emoji_code(code_id: int, selected_symbols: list[str]) -> str:
        """Check the selected emoji order."""
        return EmojiService.verify_code(code_id, selected_symbols)

    @staticmethod
    def get_users() -> list[dict[str, object]]:
        """Return all users for the admin console."""
        rows = fetch_all(
            """
            SELECT
                u.user_id,
                u.name,
                r.role_name,
                u.mail_address,
                u.phone_number,
                u.is_active,
                u.created_at,
                MAX(l.login_time) AS last_login
            FROM users AS u
            JOIN roles AS r ON u.role_id = r.role_id
            LEFT JOIN login_logs AS l
                ON u.user_id = l.user_id AND l.result = 'SUCCESS'
            GROUP BY
                u.user_id,
                u.name,
                r.role_name,
                u.mail_address,
                u.phone_number,
                u.is_active,
                u.created_at
            ORDER BY u.user_id
            """
        )
        return [dict(row) for row in rows]
