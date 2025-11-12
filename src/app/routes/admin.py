from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from functools import wraps
from ..models import Pet, User
from sqlalchemy import func
from datetime import date
from ..db import db  

bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required", "error")
            return redirect(url_for("admin.admin_login_form"))
        return f(*args, **kwargs)
    return wrapper




@bp.get("/")
def admin_home():
    if session.get("role") == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    return redirect(url_for("admin.admin_login_form"))



@bp.get("/login")
def admin_login_form():
    return render_template("admin_login.html")

@bp.post("/login")
def admin_login_submit():
    username = "admin"
    password = "supersecret"
    form_user = request.form.get("username")
    form_pass = request.form.get("password")
    if form_user==username and form_pass==password:
        session["user_id"] = 0
        session["role"] = "admin"
        flash("Logged in as admin", "success")
        return redirect(url_for("admin.admin_dashboard"))
    flash("Invalid admin credentials", "error")
    return redirect(url_for("admin.admin_login_form"))

@bp.post("/logout")
def admin_logout():
    session.pop("user_id", None)
    session.pop("role", None)
    flash("Logged out", "success")
    return redirect(url_for("admin.admin_login_form"))

@bp.get("/dashboard")
@admin_required
def admin_dashboard():
    stats = {
        "available": Pet.query.filter_by(adopted=False).count(),
        "adopted": Pet.query.filter_by(adopted=True).count()
    }
    today = date.today()
    user_stats = {
        "total_users": User.query.count(),
        "created_today": User.query.filter(func.date(User.created_at)==today).count(),
        "active_today": User.query.filter(func.date(User.created_at)==today).count()  # replace with last_login if you track
    }
    return render_template("admin_dashboard.html", stats=stats, user_stats=user_stats, active='dashboard')

@bp.get("/charts")
@admin_required
def admin_charts():
    # Species count
    species_counts = {row[0]: row[1] for row in Pet.query.with_entities(Pet.species, func.count(Pet.id)).group_by(Pet.species).all()}
    # Age count
    age_counts = {row[0]: row[1] for row in Pet.query.with_entities(Pet.age, func.count(Pet.id)).group_by(Pet.age).all()}
    # Users created over last 7 days (example)
    from datetime import timedelta
    users_counts = {}
    for i in range(7):
        day = date.today() - timedelta(days=i)
        count = User.query.filter(func.date(User.created_at)==day).count()
        users_counts[str(day)] = count

    return render_template("admin_charts.html", species_counts=species_counts, age_counts=age_counts, users_counts=users_counts, active='charts')

@bp.get("/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin_users.html", users=users, active='users')

@bp.get("/pets")
@admin_required
def admin_pets():
    pets = Pet.query.order_by(Pet.created_at.desc()).all()
    return render_template("admin_pets.html", pets=pets, active='pets')


@bp.post("/users/delete/<int:user_id>")
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} deleted.", "success")
    return redirect(url_for("admin.admin_users"))

@bp.post("/pets/delete/<int:pet_id>")
@admin_required
def admin_delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash(f"Pet {pet.name} deleted.", "success")
    return redirect(url_for("admin.admin_pets"))
