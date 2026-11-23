from app import db

class User(db.Model):
    __tablename__="users"
    
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password_hash = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(20),default="user",nullable=False)

class Record(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    course = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.Text,nullable=False)
    owner_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
