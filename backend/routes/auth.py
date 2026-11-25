from flask import Blueprint,request,jsonify
from app import db,bcrypt
from models import User
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from utils.auth_guard import login_required,admin_required
from flask import g


auth_bp =Blueprint("auth",__name__)
@auth_bp.route("/register",methods=["POST"])

def register():
    data = request.get_json(silent=True)
    
    if not isinstance(data,dict):
        return jsonify({
            "success":False,
            "data":None,
            "error":"Invalid JSON data"
        }),400
        
    username=data.get("username")
    password=data.get("password")
    
    if not isinstance(username,str) or not isinstance(password,str):
        return jsonify({
            "success":False,
            "data":None,
            "error":"Username and password are required"
        }),400
    username = username.strip()

    if not username or len(password) < 8:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Enter a username and a password of at least 8 characters"
        }), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Username already exists"
        }), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        password_hash=hashed_password,
        role="user"
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "success": True,
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role
        },
        "error": None
    }), 201
@auth_bp.route("/login", methods=["POST"])

def login():
    data=request.get_json(silent=True)
    
    if not isinstance(data,dict):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid JSON data"
        }),400
        
    username=data.get("username")
    password=data.get("password")
    
    if not isinstance(username,str) or not isinstance(password,str):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Username and password are required"
        }),400
        
    user=User.query.filter_by(username=username.strip()).first()
    if not user or not bcrypt.check_password_hash(user.password_hash,password):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid username or password"
        }),401
        
    token=jwt.encode(
        {
            "sub": str(user.id),
            "role": user.role,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
        },
        current_app.config["JWT_SECRET"],
        algorithm="HS256"
    )
    
    responce=jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        },
        "error": None
    })
    
    
    responce.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=current_app.config["COOKIE_SECURE"],
        samesite="Lax",
        max_age=900,
        path="/"
    )
    
    return responce,200


@auth_bp.route("/me", methods=["GET"])
@login_required
def get_current_user():
    user=g.current_user
    
    
    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "role": user.role

    },
    "error": None}),200
    
    

@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({
        "success": True,
        "data": None,
        "error": None
    })

    response.delete_cookie(
        "access_token",
        path="/",
        secure=current_app.config["COOKIE_SECURE"],
        httponly=True,
        samesite="Lax"
    )

    return response, 200



@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid JSON data"
        }), 400

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not isinstance(old_password, str) or not isinstance(new_password, str):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Both passwords are required"
        }), 400

    user = g.current_user

    if not bcrypt.check_password_hash(user.password_hash, old_password):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Current password is incorrect"
        }), 401

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "data": None,
            "error": "New password must be at least 8 characters"
        }), 400

    if bcrypt.check_password_hash(user.password_hash, new_password):
        return jsonify({
            "success": False,
            "data": None,
            "error": "New password must be different"
        }), 400

    user.password_hash = bcrypt.generate_password_hash(
        new_password
    ).decode("utf-8")

    db.session.commit()

    response = jsonify({
        "success": True,
        "data": None,
        "error": None
    })

    response.delete_cookie(
        "access_token",
        path="/",
        secure=current_app.config["COOKIE_SECURE"],
        httponly=True,
        samesite="Lax"
    )

    return response, 200



@auth_bp.route("/admin-check", methods=["GET"])
@admin_required
def admin_check():
    return jsonify({
        "success": True,
        "data": {
            "message": "Welcome Admin!",
            "role": g.current_user.role
        },
        "error": None
    }), 200
