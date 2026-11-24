import socket
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config

db=SQLAlchemy()
bcrypt=Bcrypt()

def create_app():
    app =Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
    db.init_app(app)
    bcrypt.init_app(app)
    
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    
    @app.route("/api/v1/health", methods=["GET"])
    
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            database_ok=True
        except SQLAlchemyError:
            db.session.rollback()
            database_ok=False
         
        return jsonify({
            "hostname": socket.gethostname(),
            "ip": app.config["LAB_IP"],
            "db": database_ok
        }), 200
   
    return app