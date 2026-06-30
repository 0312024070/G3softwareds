# ソースコード内容（修正版）
このファイルは、VS Codeで開くプロジェクト内の主要ソースコードを一覧化したものです。
今回の修正版では、ログイン画面に「新規登録」と「パスワードを忘れた場合」の画面遷移と処理を追加しています。

## .editorconfig

```
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4

[*.{html,css,js}]
indent_size = 2
```

## .vscode/launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Flask emoji_auth_system",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/app.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

## .vscode/settings.json

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,
  "editor.tabSize": 4,
  "files.encoding": "utf8"
}
```

## CODING_RULES.md

```markdown
# プログラミング規約

## 1. 命名規則

| 対象 | 規則 | 例 |
|---|---|---|
| クラス名 | PascalCase | AuthService |
| 関数名 | snake_case | verify_password |
| 変数名 | snake_case | user_id |
| 定数名 | UPPER_SNAKE_CASE | CODE_EXPIRATION_MINUTES |
| HTMLファイル名 | snake_case | emoji_auth.html |

## 2. ファイル分割

- `routes/`: URLごとの画面制御を担当する。
- `services/`: 認証、絵文字コード、通知、ログなどの業務処理を担当する。
- `templates/`: HTMLテンプレートを保存する。
- `static/`: CSS、JavaScriptを保存する。
- `database.py`: SQLite接続とDB共通処理を担当する。

## 3. セキュリティ規約

- パスワードは必ずハッシュ化する。
- SQLは必ずプレースホルダを用いて実行する。
- 認証コードは5分で期限切れにする。
- 一度使った認証コードは再利用できないようにする。
- ログイン失敗・成功・タイムアウトを履歴として残す。

## 4. コーディング規約

- 1つの関数に複数の責任を持たせない。
- 画面処理と認証ロジックを混在させない。
- 重要な関数にはdocstringを書く。
- 例外発生時は利用者向けメッセージを表示する。
- コメントは「なぜそうするか」が分かる内容にする。
```

## README.md

```markdown
# 絵文字シャッフル認証システム

株式会社村田サービス向けの「ID・パスワード認証 + 絵文字シャッフル認証」による二要素認証システムのサンプル実装です。  
VS Code で開発・実行しやすいように、Flask + SQLite 構成で作成しています。

## 1. 実装した機能

- ユーザーID・パスワードによるログイン
- 5分間有効な絵文字認証コードの生成
- 絵文字ボタンのランダムシャッフル表示
- 通知された順番どおりに絵文字を選択する二要素認証
- ログイン成功・失敗・タイムアウトの履歴保存
- 管理者用のユーザー一覧画面
- 管理者用の認証ログ履歴画面

## 2. VS Code での実行手順

### 手順1: フォルダを開く

VS Code で `emoji_auth_system` フォルダを開きます。

### 手順2: 仮想環境を作成する

```bash
python -m venv .venv
```

### 手順3: 仮想環境を有効化する

PowerShell の場合:

```bash
.venv\Scripts\Activate.ps1
```

コマンドプロンプトの場合:

```bash
.venv\Scripts\activate.bat
```

### 手順4: 必要なライブラリを入れる

```bash
pip install -r requirements.txt
```

### 手順5: データベースを初期化する

```bash
python init_db.py
```

### 手順6: Flask を起動する

```bash
python app.py
```

ブラウザで次を開きます。

```text
http://127.0.0.1:5000
```

## 3. 動作確認用アカウント

| 種別 | ユーザーID | パスワード |
|---|---|---|
| 利用者 | murata_taro | password123 |
| 管理者 | admin | admin123 |
| 利用者 | tanaka_ken | password123 |

## 4. フォルダ構成

```text
emoji_auth_system/
├─ app.py
├─ config.py
├─ database.py
├─ init_db.py
├─ models.py
├─ requirements.txt
├─ pyproject.toml
├─ .editorconfig
├─ .vscode/
│  ├─ launch.json
│  └─ settings.json
├─ routes/
│  ├─ __init__.py
│  ├─ admin_routes.py
│  └─ auth_routes.py
├─ services/
│  ├─ __init__.py
│  ├─ auth_service.py
│  ├─ emoji_service.py
│  ├─ log_service.py
│  └─ notification_service.py
├─ static/
│  ├─ css/style.css
│  └─ js/emoji_auth.js
└─ templates/
   ├─ admin_logs.html
   ├─ admin_users.html
   ├─ base.html
   ├─ emoji_auth.html
   ├─ login.html
   └─ menu.html
```

## 5. プログラミング規約

- Python は PEP8 を基本とする。
- クラス名は `PascalCase` とする。
- 関数名・変数名は `snake_case` とする。
- 定数は `UPPER_SNAKE_CASE` とする。
- 画面処理、認証処理、DB処理を分離する。
- SQL 文はパラメータバインドを使用し、文字列連結で値を埋め込まない。
- パスワードは平文保存せず、ハッシュ化して保存する。
- 認証コードには有効期限と使用済みフラグを持たせる。

## 6. 注意

このソースコードは授業課題・プロトタイプ用です。実運用する場合は、HTTPS、メール送信設定、CSRF対策、試行回数制限、監査ログ強化などを追加してください。


## 追加修正版の内容

この修正版では、ログイン画面に以下の機能を追加しています。

- 「新規登録」リンク
- 「パスワードを忘れた場合」リンク
- 新規登録画面 `/register`
- パスワード再設定画面 `/forgot-password`

### 起動方法

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
python app.py
```

ブラウザで以下を開きます。

```text
http://127.0.0.1:5000
```

※ `requirements.txt` が見つからない場合は、`app.py` と `requirements.txt` が直接見えるフォルダを VS Code で開いてください。
```

## app.py

```python
"""Application entry point for the emoji shuffle authentication system."""

from flask import Flask

from config import SECRET_KEY
from database import close_db
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.teardown_appcontext(close_db)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
```

## config.py

```python
"""Application configuration."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "emoji_auth.db"

SECRET_KEY = "change-this-secret-key-for-production"
CODE_EXPIRATION_MINUTES = 5
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
```

## database.py

```python
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
```

## init_db.py

```python
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
```

## models.py

```python
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
```

## pyproject.toml

```toml
[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I"]
```

## requirements.txt

```text
Flask==3.0.3
Werkzeug==3.0.3
```

## routes/__init__.py

```python

```

## routes/admin_routes.py

```python
"""Routes for the administrator console."""

from functools import wraps
from typing import Callable, TypeVar

from flask import Blueprint, flash, redirect, render_template, session, url_for

from services.auth_service import AuthService
from services.log_service import LogService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ViewFunction = TypeVar("ViewFunction", bound=Callable[..., str])


def admin_required(view: ViewFunction) -> ViewFunction:
    """Allow only admin users to access the decorated route."""

    @wraps(view)
    def wrapped_view(*args: object, **kwargs: object) -> str:
        if session.get("role_name") != "admin":
            flash("管理者のみアクセスできます。", "error")
            return redirect(url_for("auth.menu"))
        return view(*args, **kwargs)

    return wrapped_view  # type: ignore[return-value]


@admin_bp.route("/users")
@admin_required
def users() -> str:
    """Show user list and authentication settings."""
    user_list = AuthService.get_users()
    return render_template("admin_users.html", users=user_list)


@admin_bp.route("/logs")
@admin_required
def logs() -> str:
    """Show authentication logs."""
    login_logs = LogService.get_recent_logs()
    return render_template("admin_logs.html", logs=login_logs)
```

## routes/auth_routes.py

```python
"""Routes for login and emoji authentication."""

from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import generate_password_hash

from config import CODE_EXPIRATION_MINUTES
from database import execute_query, fetch_one
from services.auth_service import AuthService
from services.emoji_service import EmojiService
from services.log_service import LogService

auth_bp = Blueprint("auth", __name__)


def get_access_ip() -> str:
    """Return the client IP address."""
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")


@auth_bp.route("/")
def index() -> str:
    """Redirect to login or menu."""
    if "user_id" in session:
        return redirect(url_for("auth.menu"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    """Show login form and process ID/password authentication."""
    if request.method == "GET":
        return render_template("login.html")

    user_id = request.form.get("user_id", "").strip()
    password = request.form.get("password", "")

    user = AuthService.verify_password(user_id, password)
    if user is None:
        LogService.save_log(user_id or "unknown", "FAILED_PASSWORD", get_access_ip())
        flash("ユーザーIDまたはパスワードが正しくありません。", "error")
        return render_template("login.html")

    code = AuthService.start_emoji_auth(user)
    session["pending_user_id"] = user["user_id"]
    session["pending_code_id"] = code["code_id"]

    return redirect(url_for("auth.emoji_auth"))


def get_user_role_id(role_name: str) -> int | None:
    """Return a role ID by role name."""
    role = fetch_one(
        "SELECT role_id FROM roles WHERE role_name = ?",
        (role_name,),
    )
    if role is None:
        return None
    return int(role["role_id"])


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str:
    """Show user registration form and create a new account."""
    if request.method == "GET":
        return render_template("register.html", form={})

    form = {
        "user_id": request.form.get("user_id", "").strip(),
        "name": request.form.get("name", "").strip(),
        "mail_address": request.form.get("mail_address", "").strip(),
        "phone_number": request.form.get("phone_number", "").strip(),
    }
    password = request.form.get("password", "")
    password_confirm = request.form.get("password_confirm", "")

    if not form["user_id"] or not form["name"] or not form["mail_address"] or not password:
        flash("必須項目を入力してください。", "error")
        return render_template("register.html", form=form)

    if password != password_confirm:
        flash("パスワードが一致しません。", "error")
        return render_template("register.html", form=form)

    if len(password) < 8:
        flash("パスワードは8文字以上で入力してください。", "error")
        return render_template("register.html", form=form)

    existing_user = fetch_one(
        "SELECT user_id FROM users WHERE user_id = ?",
        (form["user_id"],),
    )
    if existing_user is not None:
        flash("このユーザーIDはすでに使用されています。", "error")
        return render_template("register.html", form=form)

    role_id = get_user_role_id("user")
    if role_id is None:
        flash("権限情報が見つかりません。python init_db.py を実行してください。", "error")
        return render_template("register.html", form=form)

    execute_query(
        """
        INSERT INTO users
            (user_id, name, password_hash, role_id, mail_address,
             phone_number, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            form["user_id"],
            form["name"],
            generate_password_hash(password),
            role_id,
            form["mail_address"],
            form["phone_number"],
            1,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    flash("アカウントを登録しました。ログインしてください。", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password() -> str:
    """Show password reset form and update the password."""
    if request.method == "GET":
        return render_template("forgot_password.html", form={})

    form = {
        "user_id": request.form.get("user_id", "").strip(),
        "mail_address": request.form.get("mail_address", "").strip(),
    }
    new_password = request.form.get("new_password", "")
    password_confirm = request.form.get("password_confirm", "")

    if not form["user_id"] or not form["mail_address"] or not new_password:
        flash("必須項目を入力してください。", "error")
        return render_template("forgot_password.html", form=form)

    if new_password != password_confirm:
        flash("パスワードが一致しません。", "error")
        return render_template("forgot_password.html", form=form)

    if len(new_password) < 8:
        flash("パスワードは8文字以上で入力してください。", "error")
        return render_template("forgot_password.html", form=form)

    user = fetch_one(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ? AND mail_address = ? AND is_active = 1
        """,
        (form["user_id"], form["mail_address"]),
    )
    if user is None:
        flash("ユーザーIDまたはメールアドレスが正しくありません。", "error")
        return render_template("forgot_password.html", form=form)

    execute_query(
        "UPDATE users SET password_hash = ? WHERE user_id = ?",
        (generate_password_hash(new_password), form["user_id"]),
    )

    flash("パスワードを再設定しました。新しいパスワードでログインしてください。", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/emoji-auth", methods=["GET", "POST"])
def emoji_auth() -> str:
    """Show and verify the emoji authentication screen."""
    pending_user_id = session.get("pending_user_id")
    pending_code_id = session.get("pending_code_id")

    if pending_user_id is None or pending_code_id is None:
        flash("ログイン画面からやり直してください。", "error")
        return redirect(url_for("auth.login"))

    code = EmojiService.get_code(int(pending_code_id))
    if code is None:
        flash("認証コードが見つかりません。", "error")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        if EmojiService.is_expired(code):
            LogService.save_log(str(pending_user_id), "TIMEOUT", get_access_ip())
            session.pop("pending_user_id", None)
            session.pop("pending_code_id", None)
            flash("認証コードの有効期限が切れました。再ログインしてください。", "error")
            return redirect(url_for("auth.login"))

        return render_template(
            "emoji_auth.html",
            target_symbols=code["symbol_order"],
            shuffled_symbols=EmojiService.get_shuffled_symbols(),
            expiration_minutes=CODE_EXPIRATION_MINUTES,
        )

    selected_value = request.form.get("selected_symbols", "")
    selected_symbols = [symbol for symbol in selected_value.split(",") if symbol]
    result = AuthService.check_emoji_code(int(pending_code_id), selected_symbols)

    if result == "SUCCESS":
        user = AuthService.find_user(str(pending_user_id))
        if user is None:
            flash("ユーザー情報が見つかりません。", "error")
            return redirect(url_for("auth.login"))

        session["user_id"] = user["user_id"]
        session["name"] = user["name"]
        session["role_name"] = user["role_name"]
        session.pop("pending_user_id", None)
        session.pop("pending_code_id", None)
        LogService.save_log(str(user["user_id"]), "SUCCESS", get_access_ip())
        flash("ログインに成功しました。", "success")
        return redirect(url_for("auth.menu"))

    if result == "EXPIRED":
        LogService.save_log(str(pending_user_id), "TIMEOUT", get_access_ip())
        session.pop("pending_user_id", None)
        session.pop("pending_code_id", None)
        flash("認証コードの有効期限が切れました。再ログインしてください。", "error")
        return redirect(url_for("auth.login"))

    LogService.save_log(str(pending_user_id), "FAILED_EMOJI", get_access_ip())
    flash("絵文字の順番が正しくありません。もう一度入力してください。", "error")
    return render_template(
        "emoji_auth.html",
        target_symbols=code["symbol_order"],
        shuffled_symbols=EmojiService.get_shuffled_symbols(),
        expiration_minutes=CODE_EXPIRATION_MINUTES,
    )


@auth_bp.route("/menu")
def menu() -> str:
    """Show the menu page after successful login."""
    if "user_id" not in session:
        flash("ログインしてください。", "error")
        return redirect(url_for("auth.login"))
    return render_template("menu.html")


@auth_bp.route("/logout")
def logout() -> str:
    """Clear the login session."""
    session.clear()
    flash("ログアウトしました。", "success")
    return redirect(url_for("auth.login"))
```

## run_app.bat

```bat
@echo off
REM VS Code Terminal or Command Prompt from this folder
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python init_db.py
python app.py
```

## services/__init__.py

```python

```

## services/auth_service.py

```python
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
```

## services/emoji_service.py

```python
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
```

## services/log_service.py

```python
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
```

## services/notification_service.py

```python
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
```

## static/css/style.css

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #f4f7fb;
  color: #172033;
  font-family: "Yu Gothic", "Meiryo", sans-serif;
}

.topbar {
  align-items: center;
  background: #071229;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  min-height: 64px;
  padding: 0 32px;
}

.brand {
  color: #18a7db;
  font-size: 20px;
  font-weight: 700;
}

.topbar a {
  color: #ffffff;
  margin-left: 20px;
  text-decoration: none;
}

main {
  padding: 32px;
}

.message-area {
  margin: 0 auto 20px;
  max-width: 1080px;
}

.message {
  border-radius: 8px;
  margin-bottom: 8px;
  padding: 12px 16px;
}

.message.success {
  background: #e3f8ed;
  color: #17613a;
}

.message.error {
  background: #ffe8e8;
  color: #9f2222;
}

.login-layout {
  background: #ffffff;
  border-radius: 18px;
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  margin: 30px auto;
  max-width: 1080px;
  min-height: 600px;
  overflow: hidden;
}

.login-left {
  background: #071229;
  color: #ffffff;
  padding: 88px 56px;
}

.login-left h1 {
  font-size: 42px;
  line-height: 1.35;
}

.login-left p {
  color: #c0c9d8;
  line-height: 1.8;
}

.login-card {
  padding: 88px 72px;
}

.login-card h2,
.auth-card h2,
.admin-card h1,
.menu-card h1 {
  margin-top: 0;
}

.sub-text,
.info-text {
  color: #667085;
}

label {
  display: block;
  font-weight: 700;
  margin: 24px 0 8px;
}

input[type="text"],
input[type="password"],
input[type="email"] {
  border: 1px solid #d9e1ec;
  border-radius: 8px;
  font-size: 16px;
  padding: 14px;
  width: 100%;
}

.form-row {
  align-items: center;
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.check-label {
  font-weight: 400;
  margin: 0;
}

.text-link {
  color: #1687bd;
  text-decoration: none;
}

.primary-button,
.secondary-button {
  border: 0;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 700;
  padding: 14px 20px;
}

.primary-button {
  background: #071229;
  color: #ffffff;
  width: 100%;
}

.secondary-button {
  background: #e8eef6;
  color: #172033;
}

.auth-wrapper {
  align-items: center;
  display: grid;
  gap: 32px;
  grid-template-columns: 1fr 300px;
  margin: 20px auto;
  max-width: 1100px;
}

.auth-card,
.admin-card,
.menu-card {
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
  padding: 36px;
}

.service-label {
  color: #1687bd;
  font-weight: 700;
}

.selected-panel {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 24px 0;
}

.selected-slot {
  align-items: center;
  border: 2px solid #cfd9e6;
  border-radius: 12px;
  display: flex;
  font-size: 32px;
  height: 64px;
  justify-content: center;
  width: 64px;
}

.emoji-grid {
  background: #eef3f9;
  border-radius: 22px;
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(4, 1fr);
  margin: 20px auto;
  max-width: 520px;
  padding: 20px;
}

.emoji-button {
  background: #ffffff;
  border: 1px solid #d5deeb;
  border-radius: 10px;
  cursor: pointer;
  font-size: 30px;
  padding: 12px;
}

.emoji-button.selected,
.emoji-button:disabled {
  background: #bde7f8;
  cursor: not-allowed;
}

.button-row {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr 1fr;
}

.limit-text {
  color: #d13d3d;
  font-weight: 700;
  text-align: center;
}

.phone-mock {
  background: #071229;
  border-radius: 38px;
  padding: 40px 24px;
}

.phone-screen {
  background: #ffffff;
  border-radius: 24px;
  padding: 24px;
}

.phone-small {
  color: #7f8ea3;
  font-size: 12px;
}

.phone-code {
  background: #f4f7fb;
  border-radius: 10px;
  display: flex;
  font-size: 28px;
  gap: 12px;
  justify-content: center;
  padding: 10px;
}

.admin-card {
  margin: 20px auto;
  max-width: 1100px;
  overflow-x: auto;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  border-bottom: 1px solid #edf0f5;
  padding: 14px;
  text-align: left;
}

th {
  background: #eef3f9;
}

.status {
  border-radius: 999px;
  display: inline-block;
  font-weight: 700;
  padding: 6px 12px;
}

.success-status {
  background: #dff8e8;
  color: #157347;
}

.error-status {
  background: #ffe4e4;
  color: #b42318;
}

.menu-card {
  margin: 40px auto;
  max-width: 720px;
}

.primary-link,
.secondary-link {
  border-radius: 8px;
  display: inline-block;
  margin-right: 12px;
  padding: 12px 16px;
  text-decoration: none;
}

.primary-link {
  background: #071229;
  color: #ffffff;
}

.secondary-link {
  background: #e8eef6;
  color: #172033;
}

@media (max-width: 900px) {
  .login-layout,
  .auth-wrapper {
    grid-template-columns: 1fr;
  }

  .phone-mock {
    max-width: 320px;
  }
}


.account-guide {
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 820px) {
  main {
    padding: 16px;
  }

  .login-layout,
  .auth-wrapper {
    grid-template-columns: 1fr;
  }

  .login-left,
  .login-card {
    padding: 40px 28px;
  }

  .form-row {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;
  }
}
```

## static/js/emoji_auth.js

```javascript
const maxSelectionCount = 3;
const selectedSymbols = [];

const hiddenInput = document.getElementById("selectedSymbols");
const slots = document.querySelectorAll(".selected-slot");
const buttons = document.querySelectorAll(".emoji-button");
const clearButton = document.getElementById("clearButton");
const form = document.getElementById("emojiForm");

function refreshSelectedPanel() {
  slots.forEach((slot, index) => {
    slot.textContent = selectedSymbols[index] || "";
  });
  hiddenInput.value = selectedSymbols.join(",");
}

function clearSelection() {
  selectedSymbols.length = 0;
  buttons.forEach((button) => {
    button.disabled = false;
    button.classList.remove("selected");
  });
  refreshSelectedPanel();
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    if (selectedSymbols.length >= maxSelectionCount) {
      return;
    }

    selectedSymbols.push(button.dataset.symbol);
    button.disabled = true;
    button.classList.add("selected");
    refreshSelectedPanel();
  });
});

clearButton.addEventListener("click", clearSelection);

form.addEventListener("submit", (event) => {
  if (selectedSymbols.length !== maxSelectionCount) {
    event.preventDefault();
    alert("3つの絵文字を順番に選択してください。");
  }
});
```

## templates/admin_logs.html

```html
{% extends "base.html" %}
{% block content %}
<section class="admin-card">
  <h1>認証ログ履歴</h1>
  <table>
    <thead>
      <tr>
        <th>ログID</th>
        <th>ユーザーID</th>
        <th>認証日時</th>
        <th>認証結果</th>
        <th>アクセス元IP</th>
      </tr>
    </thead>
    <tbody>
      {% for log in logs %}
        <tr>
          <td>{{ log.log_id }}</td>
          <td>{{ log.user_id }}</td>
          <td>{{ log.login_time }}</td>
          <td>{{ log.result }}</td>
          <td>{{ log.access_ip }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</section>
{% endblock %}
```

## templates/admin_users.html

```html
{% extends "base.html" %}
{% block content %}
<section class="admin-card">
  <h1>ユーザー一覧と認証設定</h1>
  <table>
    <thead>
      <tr>
        <th>ユーザーID</th>
        <th>氏名</th>
        <th>権限</th>
        <th>メールアドレス</th>
        <th>最終ログイン</th>
        <th>アカウント有効</th>
      </tr>
    </thead>
    <tbody>
      {% for user in users %}
        <tr>
          <td>{{ user.user_id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.role_name }}</td>
          <td>{{ user.mail_address }}</td>
          <td>{{ user.last_login or '-' }}</td>
          <td>
            {% if user.is_active %}
              <span class="status success-status">有効</span>
            {% else %}
              <span class="status error-status">無効</span>
            {% endif %}
          </td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</section>
{% endblock %}
```

## templates/base.html

```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title | default('Murata Service 認証システム') }}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <header class="topbar">
    <div class="brand">▰ Murata Service</div>
    <nav>
      {% if session.get('user_id') %}
        <a href="{{ url_for('auth.menu') }}">メニュー</a>
        {% if session.get('role_name') == 'admin' %}
          <a href="{{ url_for('admin.users') }}">ユーザー管理</a>
          <a href="{{ url_for('admin.logs') }}">認証ログ</a>
        {% endif %}
        <a href="{{ url_for('auth.logout') }}">ログアウト</a>
      {% endif %}
    </nav>
  </header>

  <main>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <div class="message-area">
          {% for category, message in messages %}
            <div class="message {{ category }}">{{ message }}</div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}

    {% block content %}{% endblock %}
  </main>
</body>
</html>
```

## templates/emoji_auth.html

```html
{% extends "base.html" %}
{% block content %}
<section class="auth-wrapper">
  <div class="auth-card">
    <p class="service-label">■ Murata Service データ分析基盤</p>
    <h2>セキュリティコードの確認（二要素認証）</h2>
    <p>
      登録端末へ届いた通知を確認し、指定された3つの絵文字を
      順番どおりに選択してください。
    </p>

    <div class="selected-panel" id="selectedPanel">
      <span class="selected-slot"></span>
      <span class="selected-slot"></span>
      <span class="selected-slot"></span>
    </div>

    <p class="info-text">画面表示ごとに絵文字配置がランダムにシャッフルされます。</p>

    <form method="post" id="emojiForm">
      <input type="hidden" name="selected_symbols" id="selectedSymbols">

      <div class="emoji-grid">
        {% for symbol in shuffled_symbols %}
          <button class="emoji-button" type="button" data-symbol="{{ symbol }}">
            {{ symbol }}
          </button>
        {% endfor %}
      </div>

      <div class="button-row">
        <button class="secondary-button" type="button" id="clearButton">入力を消す</button>
        <button class="primary-button" type="submit">認証する</button>
      </div>
    </form>

    <p class="limit-text">有効期限: {{ expiration_minutes }}分</p>
  </div>

  <aside class="phone-mock">
    <div class="phone-screen">
      <p class="phone-small">メッセージ | 現在</p>
      <h3>社内認証システム</h3>
      <p>【村田サービス】認証用マジック・キーワードです。</p>
      <div class="phone-code">
        {% for symbol in target_symbols %}
          <span>{{ symbol }}</span>
        {% endfor %}
      </div>
    </div>
  </aside>
</section>
<script src="{{ url_for('static', filename='js/emoji_auth.js') }}"></script>
{% endblock %}
```

## templates/forgot_password.html

```html
{% extends "base.html" %}
{% block content %}
<section class="login-layout">
  <div class="login-left">
    <h1>パスワード<br>再設定</h1>
    <p>登録済みのユーザーIDとメールアドレスを確認し、新しいパスワードを設定します。</p>
  </div>

  <div class="login-card">
    <h2>パスワードを忘れた場合</h2>
    <p class="sub-text">本人確認のため、ユーザーIDとメールアドレスを入力してください。</p>

    <form method="post" action="{{ url_for('auth.forgot_password') }}">
      <label for="user_id">ユーザーID</label>
      <input id="user_id" name="user_id" type="text" value="{{ form.user_id if form else '' }}" required>

      <label for="mail_address">メールアドレス</label>
      <input id="mail_address" name="mail_address" type="email" value="{{ form.mail_address if form else '' }}" required>

      <label for="new_password">新しいパスワード</label>
      <input id="new_password" name="new_password" type="password" placeholder="8文字以上" required>

      <label for="password_confirm">新しいパスワード確認</label>
      <input id="password_confirm" name="password_confirm" type="password" placeholder="もう一度入力" required>

      <button class="primary-button" type="submit">パスワードを再設定する</button>
    </form>

    <p class="sub-text account-guide">
      <a class="text-link" href="{{ url_for('auth.login') }}">ログイン画面に戻る</a>
    </p>
  </div>
</section>
{% endblock %}
```

## templates/login.html

```html
{% extends "base.html" %}
{% block content %}
<section class="login-layout">
  <div class="login-left">
    <h1>データ分析<br>プラットフォーム</h1>
    <p>社内データへ安全にアクセスするための統合認証ゲートウェイです。</p>
  </div>

  <div class="login-card">
    <h2>ログイン</h2>
    <p class="sub-text">ユーザーIDとパスワードを入力してください。</p>

    <form method="post" action="{{ url_for('auth.login') }}">
      <label for="user_id">ユーザーID</label>
      <input id="user_id" name="user_id" type="text" placeholder="例: murata_taro" required>

      <label for="password">パスワード</label>
      <input id="password" name="password" type="password" required>

      <div class="form-row">
        <label class="check-label">
          <input type="checkbox" name="remember_me">
          ログイン状態を保存
        </label>
        <a class="text-link" href="{{ url_for('auth.forgot_password') }}">パスワードを忘れた場合</a>
      </div>

      <button class="primary-button" type="submit">次へ進む</button>
    </form>

    <p class="sub-text account-guide">
      アカウントを持っていない場合は
      <a class="text-link" href="{{ url_for('auth.register') }}">新規登録</a>
    </p>
  </div>
</section>
{% endblock %}
```

## templates/menu.html

```html
{% extends "base.html" %}
{% block content %}
<section class="menu-card">
  <h1>ログイン完了</h1>
  <p>{{ session.get('name') }} さん、認証に成功しました。</p>

  <div class="menu-actions">
    {% if session.get('role_name') == 'admin' %}
      <a class="primary-link" href="{{ url_for('admin.users') }}">管理コンソールを開く</a>
      <a class="secondary-link" href="{{ url_for('admin.logs') }}">認証ログを見る</a>
    {% else %}
      <p>社内システムメニューへ進めます。</p>
    {% endif %}
  </div>
</section>
{% endblock %}
```

## templates/register.html

```html
{% extends "base.html" %}
{% block content %}
<section class="login-layout">
  <div class="login-left">
    <h1>アカウント<br>新規登録</h1>
    <p>利用者情報を入力して、新しいログインアカウントを作成します。</p>
  </div>

  <div class="login-card">
    <h2>新規登録</h2>
    <p class="sub-text">ユーザー情報を入力してください。</p>

    <form method="post" action="{{ url_for('auth.register') }}">
      <label for="user_id">ユーザーID</label>
      <input id="user_id" name="user_id" type="text" placeholder="例: yamada-taro" value="{{ form.user_id if form else '' }}" required>

      <label for="name">氏名</label>
      <input id="name" name="name" type="text" placeholder="例: 山田　太郎" value="{{ form.name if form else '' }}" required>

      <label for="mail_address">メールアドレス</label>
      <input id="mail_address" name="mail_address" type="email" placeholder="例: yamada@example.com" value="{{ form.mail_address if form else '' }}" required>

      <label for="phone_number">電話番号</label>
      <input id="phone_number" name="phone_number" type="text" placeholder="例: 090-0000-0000" value="{{ form.phone_number if form else '' }}">

      <label for="password">パスワード</label>
      <input id="password" name="password" type="password" placeholder="8文字以上" required>

      <label for="password_confirm">パスワード確認</label>
      <input id="password_confirm" name="password_confirm" type="password" placeholder="もう一度入力" required>

      <button class="primary-button" type="submit">登録する</button>
    </form>

    <p class="sub-text account-guide">
      <a class="text-link" href="{{ url_for('auth.login') }}">ログイン画面に戻る</a>
    </p>
  </div>
</section>
{% endblock %}
```
