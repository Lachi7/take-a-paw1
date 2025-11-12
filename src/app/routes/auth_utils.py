# app/routes/auth_utils.py
from functools import wraps
from flask import session, redirect, url_for, request, flash, jsonify

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login_form", next=request.path))
        return view(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":  # Simple stub, later use DB role
            return jsonify({"ok": False, "error": "admin access required"}), 403
        return f(*args, **kwargs)
    return decorated
