from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User

admin_bp = Blueprint('admin_bp', __name__)

# Decorator to enforce admin-only access
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"msg": "Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper


# Route to block a user (using PUT)
@admin_bp.route("/block/<int:user_id>", methods=["PUT"])
@admin_required
def block_user(user_id):
    u = User.query.get_or_404(user_id)
    u.is_blocked = True
    db.session.commit()
    return jsonify({"msg": f"User {u.username} blocked"}), 200

# Route to unblock a user (using PUT)
@admin_bp.route("/unblock/<int:user_id>", methods=["PUT"])
@admin_required
def unblock_user(user_id):
    u = User.query.get_or_404(user_id)
    u.is_blocked = False
    db.session.commit()
    return jsonify({"msg": f"User {u.username} unblocked"}), 200
