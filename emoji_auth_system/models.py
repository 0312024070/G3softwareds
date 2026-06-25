"""Data models used by the authentication system."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    """User entity."""

    user_id: str
    name: str
    password_hash: str
    role_id: int
    role_name: str
    mail_address: str
    phone_number: str | None
    is_active: bool


@dataclass(frozen=True)
class EmojiCode:
    """One-time emoji code entity."""

    code_id: int
    user_id: str
    symbol_order: str
    expiration_time: datetime
    used_flag: bool


@dataclass(frozen=True)
class LoginLog:
    """Login log entity."""

    log_id: int
    user_id: str
    login_time: datetime
    result: str
    access_ip: str
