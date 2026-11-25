from functools import wraps
import jwt
from flask import request,jsonify,current_app,g
from app import db
from models import User


def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        
        token=request.cookies.get("access_token")
        
        if not token:
            return jsonify({
                "success": False,
                "data": None,
                "error": "Login required"
            }),401

        try:
            payload=jwt.decode(token,current_app.config["JWT_SECRET"],algorithms=["HS256"],options={"required":["sub","exp"]})
            
            user_id=int(payload["sub"])
            user=db.session.get(User,user_id)
            
            if user is None :
                return jsonify({
                    "success": False,
                    "data": None,
                    "error": "User not found"
                }),401
                
            g.current_user=user
            
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                "success": False,
                "data": None,
                "error": "Token expired"
            }),401
            
        except (jwt.InvalidTokenError, ValueError, TypeError, KeyError):
            return jsonify({
                "success": False,
                "data": None,
                "error": "Invalid token"
            }), 401

        return func(*args, **kwargs)
    
    return wrapper


def admin_required(func):
    @login_required
    @wraps(func)
    def wrapper(*args, **kwargs):

        if g.current_user.role != "admin":
            return jsonify({
                "success": False,
                "data": None,
                "error": "Admin access required"
            }), 403

        return func(*args, **kwargs)

    return wrapper
