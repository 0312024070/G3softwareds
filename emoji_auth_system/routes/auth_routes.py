"""Routes for login, registration, and emoji authentication."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta

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

from config import CODE_EXPIRATION_MINUTES, REGISTRATION_CODE_EXPIRATION_MINUTES
from database import execute_query, fetch_one
from services.auth_service import AuthService
from services.emoji_service import EmojiService
from services.log_service import LogService
from services.notification_service import NotificationService

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


def create_verification_code() -> str:
    """Create a six-digit verification code for registration."""
    return f"{secrets.randbelow(1_000_000):06d}"


def save_pending_registration(form: dict[str, str], password: str, role_id: int) -> str:
    """Store registration data temporarily until email verification succeeds."""
    verification_code = create_verification_code()
    expiration_time = datetime.now() + timedelta(minutes=REGISTRATION_CODE_EXPIRATION_MINUTES)

    session["pending_registration"] = {
        "user_id": form["user_id"],
        "name": form["name"],
        "mail_address": form["mail_address"],
        "phone_number": form["phone_number"],
        "password_hash": generate_password_hash(password),
        "role_id": role_id,
        "verification_code": verification_code,
        "expiration_time": expiration_time.isoformat(timespec="seconds"),
    }

    return verification_code


def get_pending_registration() -> dict[str, object] | None:
    """Return pending registration data stored in the session."""
    pending = session.get("pending_registration")
    if not isinstance(pending, dict):
        return None
    return pending


def is_pending_registration_expired(pending: dict[str, object]) -> bool:
    """Return True when the pending registration verification code is expired."""
    expiration_text = str(pending.get("expiration_time", ""))
    try:
        expiration_time = datetime.fromisoformat(expiration_text)
    except ValueError:
        return True
    return datetime.now() > expiration_time


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str:
    """Show user registration form and start email verification."""
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

    existing_mail = fetch_one(
        "SELECT user_id FROM users WHERE mail_address = ?",
        (form["mail_address"],),
    )
    if existing_mail is not None:
        flash("このメールアドレスはすでに登録されています。", "error")
        return render_template("register.html", form=form)

    role_id = get_user_role_id("user")
    if role_id is None:
        flash("権限情報が見つかりません。python init_db.py を実行してください。", "error")
        return render_template("register.html", form=form)

    verification_code = save_pending_registration(form, password, role_id)
    NotificationService.send_registration_code(
        form["mail_address"],
        verification_code,
        REGISTRATION_CODE_EXPIRATION_MINUTES,
    )

    flash("入力されたメールアドレスへ確認コードを送信しました。", "success")
    return redirect(url_for("auth.verify_registration"))


@auth_bp.route("/register/verify", methods=["GET", "POST"])
def verify_registration() -> str:
    """Verify the email code and create the user account."""
    pending = get_pending_registration()
    if pending is None:
        flash("新規登録画面からやり直してください。", "error")
        return redirect(url_for("auth.register"))

    if request.method == "GET":
        return render_template(
            "verify_registration.html",
            mail_address=pending.get("mail_address"),
            expiration_minutes=REGISTRATION_CODE_EXPIRATION_MINUTES,
        )

    input_code = request.form.get("verification_code", "").strip()

    if is_pending_registration_expired(pending):
        session.pop("pending_registration", None)
        flash("確認コードの有効期限が切れました。もう一度登録してください。", "error")
        return redirect(url_for("auth.register"))

    if input_code != str(pending.get("verification_code")):
        flash("確認コードが正しくありません。", "error")
        return render_template(
            "verify_registration.html",
            mail_address=pending.get("mail_address"),
            expiration_minutes=REGISTRATION_CODE_EXPIRATION_MINUTES,
        )

    existing_user = fetch_one(
        "SELECT user_id FROM users WHERE user_id = ?",
        (str(pending["user_id"]),),
    )
    if existing_user is not None:
        session.pop("pending_registration", None)
        flash("このユーザーIDはすでに使用されています。", "error")
        return redirect(url_for("auth.register"))

    execute_query(
        """
        INSERT INTO users
            (user_id, name, password_hash, role_id, mail_address,
             phone_number, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(pending["user_id"]),
            str(pending["name"]),
            str(pending["password_hash"]),
            int(pending["role_id"]),
            str(pending["mail_address"]),
            str(pending.get("phone_number", "")),
            1,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    session.pop("pending_registration", None)
    flash("メール確認が完了しました。アカウントを登録しました。", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register/resend", methods=["POST"])
def resend_registration_code() -> str:
    """Resend the registration verification code."""
    pending = get_pending_registration()
    if pending is None:
        flash("新規登録画面からやり直してください。", "error")
        return redirect(url_for("auth.register"))

    verification_code = create_verification_code()
    expiration_time = datetime.now() + timedelta(minutes=REGISTRATION_CODE_EXPIRATION_MINUTES)
    pending["verification_code"] = verification_code
    pending["expiration_time"] = expiration_time.isoformat(timespec="seconds")
    session["pending_registration"] = pending

    NotificationService.send_registration_code(
        str(pending["mail_address"]),
        verification_code,
        REGISTRATION_CODE_EXPIRATION_MINUTES,
    )
    flash("確認コードを再送信しました。", "success")
    return redirect(url_for("auth.verify_registration"))


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
