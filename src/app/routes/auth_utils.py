from functools import wraps
from flask import session, redirect, url_for, request, flash

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login_form", next=request.path))
        return view(*args, **kwargs)
    return wrapper
