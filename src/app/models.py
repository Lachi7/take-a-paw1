# app/models.py
from datetime import datetime,timezone
from .db import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(64), primary_key=True)         # username for now
    display_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    public_contact = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    pets = db.relationship("Pet", backref="owner", lazy=True)

class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(30), nullable=False)      # Cat/Dog/Other
    breed = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    adopted = db.Column(db.Boolean, default=False, nullable=False)
    source = db.Column(db.String(30), default="catalog", nullable=False)  # catalog | user
    owner_id = db.Column(db.String(64), db.ForeignKey("users.id"), nullable=True)

    # Per-pet overrides (used when no owner or owner wants different contact)
    contact_email_override = db.Column(db.String(120), nullable=True)
    contact_phone_override = db.Column(db.String(50), nullable=True)

    #for quiz
    home_type = db.Column(db.String(50), nullable=True)
    activity_level = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.String(50), nullable=True)
    time_commitment = db.Column(db.String(50), nullable=True)
    family_situation = db.Column(db.String(50), nullable=True)
    
    # Final toggle at the listing level
    public_contact = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Favorite(db.Model):
    __tablename__ = "favorites"
    user_id = db.Column(db.String(64), db.ForeignKey("users.id"), primary_key=True)
    pet_id  = db.Column(db.Integer, db.ForeignKey("pets.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", lazy=True)
    pet  = db.relationship("Pet",  lazy=True)
