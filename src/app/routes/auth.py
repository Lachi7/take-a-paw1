# app/routes/auth.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from ..db import db
from ..models import User

bp = Blueprint("auth", __name__)

def _normalize_username(u: str) -> str:
    return (u or "").strip().lower()


# =========================
# Registration
# =========================
@bp.get("/register")
def register_form():
    return render_template("register.html")


@bp.post("/register")
def register_submit():
    data = request.get_json(silent=True) or request.form
    username = _normalize_username(data.get("username"))
    password = data.get("password")
    display_name = data.get("display_name") or username
    email = (data.get("email") or "").strip() or None
    phone = (data.get("phone") or "").strip() or None
    public_contact = str(data.get("public_contact", "true")).lower() in ("1","true","yes","on")

    if not username or not password:
        msg = "Username and password are required."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.register_form"))

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        msg = "Username already taken."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.register_form"))

    # Create new user
    user = User(username=username, display_name=display_name, email=email, phone=phone, public_contact=public_contact)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    next_url = url_for("pets.home_index")
    if request.is_json:
        return jsonify({"ok": True, "user": {"id": user.id, "display_name": user.display_name}, "next": next_url})
    flash(f"Welcome, {user.display_name}!", "success")
    return redirect(next_url)


# =========================
# Login
# =========================
@bp.get("/login")
def login_form():
    next_url = request.args.get("next") or "/"
    return render_template("login.html", next_url=next_url)


@bp.post("/login")
def login_submit():
    data = request.get_json(silent=True) or request.form
    username = _normalize_username(data.get("username"))
    password = data.get("password")

    if not username or not password:
        msg = "Username and password are required."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.login_form"))

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        msg = "Invalid username or password."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.login_form"))

    session["user_id"] = user.id
    next_url = url_for("pets.home_index")

    if request.is_json:
        return jsonify({"ok": True, "user": {"id": user.id, "display_name": user.display_name}, "next": next_url})
    flash(f"Welcome back, {user.display_name}!", "success")
    return redirect(next_url)


# =========================
# Logout
# =========================
@bp.post("/logout")
def logout():
    session.pop("user_id", None)
    flash("You are logged out.", "success")
    return redirect(url_for("pets.home_index"))


# =========================
# Current user info
# =========================
@bp.get("/me")
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"ok": False, "user": None})
    u = User.query.get(uid)
    return jsonify({"ok": True, "user": {
        "id": u.id,
        "username": u.username,
        "display_name": u.display_name,
        "email": u.email,
        "phone": u.phone,
        "public_contact": u.public_contact
    }})
