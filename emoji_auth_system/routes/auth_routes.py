"""Routes for login and emoji authentication."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from config import CODE_EXPIRATION_MINUTES
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
