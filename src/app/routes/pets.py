# app/routes/pets.py
from flask import Blueprint, flash, jsonify, redirect, request, session, render_template, url_for

from app.routes.auth_utils import login_required
from ..db import db
from ..models import Favorite, Pet, User

bp = Blueprint("pets", __name__)

def _resolve_contact(p: Pet):
    # Prefer per-pet override
    email = p.contact_email_override
    phone = p.contact_phone_override

    # Fall back to owner's contact if public and no override
    if p.owner_id and p.owner:
        if not email and p.owner.public_contact:
            email = p.owner.email
        if not phone and p.owner.public_contact:
            phone = p.owner.phone

    # Respect per-pet visibility
    if not p.public_contact:
        email = None
        phone = None

    return email, phone

def serialize_pet(p: Pet):
    email, phone = _resolve_contact(p)
    return {
        "id": p.id,
        "name": p.name,
        "species": p.species,
        "breed": p.breed,
        "age": p.age,
        "gender": p.gender,
        "location": p.location,
        "description": p.description,
        "image": p.image,
        "adopted": p.adopted,
        "source": p.source,
        "owner_id": p.owner_id,
        "public_contact": p.public_contact,
        "contact_email": email,
        "contact_phone": phone,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }

@bp.get("/pets")
def list_pets():
    pets = Pet.query.filter_by(adopted=False).order_by(Pet.created_at.desc()).all()
    return jsonify([serialize_pet(p) for p in pets])

@bp.get("/pets/<int:pet_id>")
def pet_detail(pet_id: int):
    p = Pet.query.get(pet_id)
    if not p or p.adopted:
        return jsonify({"error": "not found"}), 404
    return jsonify(serialize_pet(p))

@bp.get("/pets/search")
def search():
    species  = (request.args.get("species")  or "").strip().lower()
    breed    = (request.args.get("breed")    or "").strip().lower()
    location = (request.args.get("location") or "").strip().lower()

    q = Pet.query.filter_by(adopted=False)
    if species:  q = q.filter(Pet.species.ilike(species))
    if breed:    q = q.filter(Pet.breed.ilike(f"%{breed}%"))
    if location: q = q.filter(Pet.location.ilike(f"%{location}%"))

    pets = q.order_by(Pet.created_at.desc()).all()
    return jsonify([serialize_pet(p) for p in pets])

@bp.post("/pets")
def create_listing():
    user_id = session.get("user_id")
    if not user_id:
        if request.is_json:
            return jsonify({"ok": False, "error": "login required"}), 401
        flash("Please log in to add a pet.", "error")
        return redirect(url_for("auth.login_form", next=url_for("pets.add_pet_form")))

    data = request.get_json(silent=True) or request.form
    required = ["name","species","breed","age","gender","location","description"]
    missing = [k for k in required if not (data.get(k) or "").strip()]
    if missing:
        if request.is_json:
            return jsonify({"ok": False, "error": f"missing fields: {', '.join(missing)}"}), 400
        flash(f"Missing fields: {', '.join(missing)}", "error")
        return redirect(url_for("pets.add_pet_form"))

    pet = Pet(
        name=data["name"].strip(),
        species=data["species"].strip().capitalize(),
        breed=data["breed"].strip(),
        age=data["age"].strip(),
        gender=data["gender"].strip(),
        location=data["location"].strip(),
        description=data["description"].strip(),
        image=(data.get("image") or "https://placehold.co/900x600?text=Pet").strip(),
        adopted=False,
        source="user",
        owner_id=user_id,
        contact_email_override=(data.get("contact_email") or None),
        contact_phone_override=(data.get("contact_phone") or None),
        public_contact=bool(data.get("public_contact", True)),
    )
    db.session.add(pet)
    db.session.commit()

    # Form submissions: redirect to a real page with a flash
    if not request.is_json:
        # Choose where to go:
        next_url = request.form.get("next")  # optional hidden field in the form
        if next_url:
            flash(f"Your listing “{pet.name}” is live!", "success")
            return redirect(next_url)

        # Default: go to the new pet's page
        flash(f"Your listing “{pet.name}” is live!", "success")
        return redirect(url_for("pets.home_pet_detail", pet_id=pet.id))

    # JSON clients still get JSON:
    return jsonify({"ok": True, "pet": serialize_pet(pet)}), 201


@bp.get("/me/listings")
@login_required
def my_listings_page():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your listings.")
        return redirect(url_for("pets.home_index"))
    pets = Pet.query.filter_by(owner_id=user_id).order_by(Pet.created_at.desc()).all()
    # Reuse serializer if you prefer; passing ORM objects is fine for the fields we use
    return render_template("my_listings.html", pets=[serialize_pet(p) for p in pets])


# toggle favorite
@bp.post("/pets/<int:pet_id>/favorite")
def toggle_favorite(pet_id: int):
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to use favorites.", "error")
        return redirect(url_for("auth.login_form", next=request.path))

    user = User.query.get(user_id)
    if not user:
        # basic user record
        user = User(id=user_id, display_name=user_id)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome, {user_id}! Your profile has been created.", "success")

    pet = Pet.query.get(pet_id)
    if not pet or pet.adopted:
        flash("Pet not found or already adopted.", "error")
        next_url = request.form.get("next") or url_for("pets.home_index")
        return redirect(next_url)

    fav = Favorite.query.filter_by(user_id=user_id, pet_id=pet_id).first()
    
    if fav:
        # Remove from favorites
        db.session.delete(fav)
        action = "removed from"
    else:
        # Add to favorites
        db.session.add(Favorite(user_id=user_id, pet_id=pet_id))
        action = "added to"
    
    try:
        db.session.commit()
        flash(f"Pet {action} favorites.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error updating favorites. Please try again.", "error")
        print(f"Favorite error: {e}")

    next_url = request.form.get("next") or request.headers.get("Referer") or url_for("pets.home_index")
    return redirect(next_url)

# my favorites
# existing JSON API (keep it!)
@bp.get("/me/favorites")
def my_favorites_json():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])
    favs = Favorite.query.filter_by(user_id=user_id).all()
    pet_ids = [f.pet_id for f in favs]
    if not pet_ids:
        return jsonify([])
    pets = Pet.query.filter(Pet.id.in_(pet_ids), Pet.adopted == False).all()
    return jsonify([serialize_pet(p) for p in pets])

# new template page
@bp.get("/favorites")
def favorites_page():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to see favorites.")
        return redirect(url_for("pets.home_index"))
    favs = Favorite.query.filter_by(user_id=user_id).all()
    ids = [f.pet_id for f in favs]
    pets = Pet.query.filter(Pet.id.in_(ids), Pet.adopted == False).all() if ids else []
    return render_template("favorites.html", pets=[serialize_pet(p) for p in pets])


@bp.get("/")
def home_index():
    pets = Pet.query.filter_by(adopted=False).order_by(Pet.created_at.desc()).all()
    return render_template("index.html", pets=pets)



@bp.get("/search")
def home_search():
    species  = (request.args.get("species")  or "").strip()
    breed    = (request.args.get("breed")    or "").strip()
    location = (request.args.get("location") or "").strip()

    q = Pet.query.filter_by(adopted=False)
    if species:
        # allow partial, case-insensitive
        q = q.filter(Pet.species.ilike(f"%{species}%"))
    if breed:
        q = q.filter(Pet.breed.ilike(f"%{breed}%"))
    if location:
        q = q.filter(Pet.location.ilike(f"%{location}%"))

    pets = q.order_by(Pet.created_at.desc()).all()
    return render_template("index.html", pets=[serialize_pet(p) for p in pets])

@bp.get("/pet/<int:pet_id>")
def home_pet_detail(pet_id: int):
    p = Pet.query.get(pet_id)
    if not p or p.adopted:
        return render_template("404.html"), 404

    # Reuse your serializer so the template gets contact_* fields
    pet = serialize_pet(p)
    return render_template("pet_detail.html", pet=pet)

@bp.get("/add-pet")
@login_required
def add_pet_form():
    if not session.get("user_id"):
        # optional: force login to list
        flash("Please log in to add a pet.")
        return redirect(url_for("pets.home_index"))
    return render_template("add_pet.html")
