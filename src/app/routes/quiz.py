from flask import Blueprint, jsonify, request
from ..models import Pet

bp = Blueprint("quiz", __name__)

@bp.get("/quiz")
def quiz_info():
    return jsonify({
        "ok": True,
        "message": "Submit POST /quiz/results with JSON: {home_type, activity_level, experience, time_commitment, family_situation}"
    })

@bp.post("/quiz/results")
def quiz_results():
    data = request.get_json(silent=True) or {}
    # Minimal stub: just return top 10 available pets for now.
    pets = Pet.query.filter_by(adopted=False).order_by(Pet.created_at.desc()).limit(10).all()
    return jsonify({
        "ok": True,
        "criteria": data,
        "matches": [ {
            "id": p.id, "name": p.name, "species": p.species,
            "breed": p.breed, "location": p.location
        } for p in pets ]
    })
