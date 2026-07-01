"""Notification service.

This service sends the emoji authentication code to the user's
registered email address.  SMTP settings are read from environment
variables so that passwords are not written in the source code.
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


class NotificationService:
    """Send authentication code notifications."""

    @staticmethod
    def send_emoji_code(mail_address: str, symbols: list[str]) -> None:
        """Send the emoji code to a registered email address.

        If SMTP environment variables are not configured, the code is
        printed to the terminal as a safe fallback for classroom testing.
        """
        code_text = " ".join(symbols)
        subject = "【Murata Service】二要素認証コード"
        body = (
            "社内認証システムの認証用マジック・キーワードです。\n\n"
            f"認証コード: {code_text}\n\n"
            "有効期限内にPC画面で順番どおりに選択してください。\n"
            "心当たりがない場合は、このメールを破棄してください。\n"
        )

        if not NotificationService._is_smtp_configured():
            NotificationService._print_fallback(mail_address, code_text)
            return

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = os.environ["SMTP_FROM"]
        message["To"] = mail_address
        message.set_content(body)

        try:
            with smtplib.SMTP(
                os.environ["SMTP_SERVER"],
                int(os.environ.get("SMTP_PORT", "587")),
                timeout=10,
            ) as smtp:
                smtp.starttls()
                smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
                smtp.send_message(message)

            print("=" * 60)
            print("[通知サービス] メール送信成功")
            print(f"送信先: {mail_address}")
            print("=" * 60)
        except Exception as error:  # noqa: BLE001
            print("=" * 60)
            print("[通知サービス] メール送信に失敗しました。")
            print(f"送信先: {mail_address}")
            print(f"エラー: {error}")
            print("授業用確認のため、認証コードをターミナルにも表示します。")
            print(f"認証コード: {code_text}")
            print("=" * 60)


    @staticmethod
    def send_registration_code(mail_address: str, verification_code: str, expiration_minutes: int) -> None:
        """Send a registration verification code to an email address."""
        subject = "【Murata Service】新規登録確認コード"
        body = (
            "新規登録を完了するための確認コードです。\n\n"
            f"確認コード: {verification_code}\n\n"
            f"有効期限は{expiration_minutes}分です。\n"
            "心当たりがない場合は、このメールを破棄してください。\n"
        )

        if not NotificationService._is_smtp_configured():
            NotificationService._print_registration_fallback(mail_address, verification_code)
            return

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = os.environ["SMTP_FROM"]
        message["To"] = mail_address
        message.set_content(body)

        try:
            with smtplib.SMTP(
                os.environ["SMTP_SERVER"],
                int(os.environ.get("SMTP_PORT", "587")),
                timeout=10,
            ) as smtp:
                smtp.starttls()
                smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
                smtp.send_message(message)

            print("=" * 60)
            print("[通知サービス] 新規登録確認メール送信成功")
            print(f"送信先: {mail_address}")
            print("=" * 60)
        except Exception as error:  # noqa: BLE001
            print("=" * 60)
            print("[通知サービス] 新規登録確認メール送信に失敗しました。")
            print(f"送信先: {mail_address}")
            print(f"エラー: {error}")
            print("授業用確認のため、確認コードをターミナルにも表示します。")
            print(f"確認コード: {verification_code}")
            print("=" * 60)

    @staticmethod
    def _is_smtp_configured() -> bool:
        """Return True if SMTP settings are available."""
        required_keys = ["SMTP_SERVER", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM"]
        return all(os.environ.get(key) for key in required_keys)

    @staticmethod
    def _print_fallback(mail_address: str, code_text: str) -> None:
        """Print the code when email sending is not configured."""
        print("=" * 60)
        print("[通知サービス] SMTP未設定のため、メール送信は行いません。")
        print(f"送信先: {mail_address}")
        print(f"認証コード: {code_text}")
        print("メール送信する場合は、SMTP_SERVER / SMTP_USER / SMTP_PASSWORD / SMTP_FROM を設定してください。")
        print("=" * 60)

    @staticmethod
    def _print_registration_fallback(mail_address: str, verification_code: str) -> None:
        """Print the registration verification code when email is not configured."""
        print("=" * 60)
        print("[通知サービス] SMTP未設定のため、新規登録確認メールは送信しません。")
        print(f"送信先: {mail_address}")
        print(f"確認コード: {verification_code}")
        print("メール送信する場合は、SMTP_SERVER / SMTP_USER / SMTP_PASSWORD / SMTP_FROM を設定してください。")
        print("=" * 60)

