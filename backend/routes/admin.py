from flask import Blueprint, jsonify
from models import User
from utils.auth_guard import admin_required
admin_bp = Blueprint("admin", __name__)
@admin_bp.route("/users", methods=["GET"])
@admin_required

def get_all_users():
    users=User.query.order_by(User.id.asc()).all()

    result=[]
    for user in users:
        result.append({
            "id":user.id,
            "username":user.username,
            "role":user.role
        })

    return jsonify({
        "success": True,
        "data": result,
        "error": None
    }), 200
