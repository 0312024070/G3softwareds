"""Application configuration."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "emoji_auth.db"

SECRET_KEY = "change-this-secret-key-for-production"
CODE_EXPIRATION_MINUTES = 5
REGISTRATION_CODE_EXPIRATION_MINUTES = 10
EMOJI_CODE_LENGTH = 3

EMOJI_SYMBOLS = [
    "🐱",
    "🚀",
    "🍐",
    "🚗",
    "🍉",
    "🎸",
    "🔑",
    "💎",
    "🐼",
    "🎈",
    "🎯",
    "🔥",
]
