from flask import Blueprint,request,jsonify
from app import db,bcrypt
from models import User

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
        
    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        },
        "error": None
    }), 200
