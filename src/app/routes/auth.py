from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from ..db import db
from ..models import User

bp = Blueprint("auth", __name__)

def _normalize_username(u: str) -> str:
    return (u or "").strip().lower()

@bp.get("/login")
def login_form():
    # optional ?next=/add-pet to return after login
    next_url = request.args.get("next") or "/"
    return render_template("login.html", next_url=next_url)

@bp.post("/login")
def login_submit():
    # accept JSON or form
    data = request.get_json(silent=True) or request.form

    username = _normalize_username(data.get("username"))
    if not username:
        if request.is_json:
            return jsonify({"ok": False, "error": "username required"}), 400
        flash("Username is required.", "error")
        return redirect(url_for("auth.login_form"))

    # optional profile contact fields
    display_name = data.get("display_name") or username
    email        = (data.get("email") or "").strip() or None
    phone        = (data.get("phone") or "").strip() or None
    public_contact = str(data.get("public_contact", "true")).lower() in ("1","true","yes","on")

    user = User.query.get(username)
    if not user:
        user = User(id=username, display_name=display_name, email=email, phone=phone, public_contact=public_contact)
        db.session.add(user)
    else:
        # light upsert
        user.display_name = display_name or user.display_name
        user.email = email or user.email
        user.phone = phone or user.phone
        user.public_contact = public_contact if data.get("public_contact") is not None else user.public_contact
    db.session.commit()

    session["user_id"] = user.id

    next_url = data.get("next") or request.args.get("next") or url_for("pets.home_index")
    if request.is_json:
        return jsonify({"ok": True, "user": {"id": user.id, "display_name": user.display_name}, "next": next_url})
    flash(f"Welcome, {user.display_name}!", "success")
    return redirect(next_url)

@bp.post("/logout")
def logout():
    session.pop("user_id", None)
    flash("You are logged out.", "success")
    return redirect(url_for("pets.home_index"))

@bp.get("/me")
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"ok": False, "user": None})
    u = User.query.get(uid)
    return jsonify({"ok": True, "user": {
        "id": u.id, "display_name": u.display_name, "email": u.email, "phone": u.phone, "public_contact": u.public_contact
    }})
