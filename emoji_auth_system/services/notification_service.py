"""Notification service.

The real system would send an email or smartphone notification.
For this prototype, the code is displayed in the Flask terminal and
also shown in the smartphone mock area on the authentication screen.
"""


class NotificationService:
    """Send authentication code notifications."""

    @staticmethod
    def send_emoji_code(mail_address: str, symbols: list[str]) -> None:
        """Send the emoji code to a registered address.

        This prototype prints the message instead of sending real email.
        """
        code_text = " ".join(symbols)
        print("=" * 60)
        print("[通知サービス] 認証用マジック・キーワード")
        print(f"送信先: {mail_address}")
        print(f"認証コード: {code_text}")
        print("有効期限内にPC画面で順番どおりに選択してください。")
        print("=" * 60)
