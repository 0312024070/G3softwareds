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
