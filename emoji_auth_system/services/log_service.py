"""Service for saving and reading login logs."""

from datetime import datetime

from database import execute_query, fetch_all


class LogService:
    """Manage login history."""

    @staticmethod
    def save_log(user_id: str, result: str, access_ip: str) -> None:
        """Save a login result."""
        execute_query(
            """
            INSERT INTO login_logs (user_id, login_time, result, access_ip)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                datetime.now().isoformat(timespec="seconds"),
                result,
                access_ip,
            ),
        )

    @staticmethod
    def get_recent_logs(limit: int = 100) -> list[dict[str, object]]:
        """Return recent login logs."""
        rows = fetch_all(
            """
            SELECT log_id, user_id, login_time, result, access_ip
            FROM login_logs
            ORDER BY login_time DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in rows]
