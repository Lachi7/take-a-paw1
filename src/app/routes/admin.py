from flask import Blueprint, jsonify, session
from ..models import Pet

bp = Blueprint("admin", __name__)

@bp.get("/admin")
def admin_dashboard_json():
    available = Pet.query.filter_by(adopted=False).count()
    adopted   = Pet.query.filter_by(adopted=True).count()
    return jsonify({
        "ok": True,
        "role": "admin (stub)",
        "stats": {"available": available, "adopted": adopted}
    })

@bp.get("/admin/adoptions")
def admin_adoptions_json():
    # Adoption flow deferred by design; return empty list for now.
    return jsonify({"ok": True, "adoptions": []})
