from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from models import db,User

user_api=Blueprint("user_api", __name__)

@user_api.route("/api/register", methods=["POST"])
def register_user():
    data=request.get_json()
    if not data or not all(k in data for k in ["email", "password", "name"]):
        return jsonify({"error": "Missing required fields"}),400
    email=data["email"]
    password=data["password"]
    name=data["name"]
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}),409
    hashed_pass=generate_password_hash(password, method="pbkdf2:sha256")
    new_user=User(email=email, password=hashed_pass, name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User registered successfully"}),201
@user_api.route("/api/login",methods=["POST"])
def login_user_api():
    data=request.get_json()    
    if not data or not all(k in data for k in ["email", "password"]):
        return jsonify({"error": "Missing email or password"}),400    
    user = User.query.filter_by(email=data["email"]).first()    
    if user and check_password_hash(user.password, data["password"]):
        login_user(user)
        return jsonify({"message": "Login successful"}),200    
    return jsonify({"error": "Invalid credentials"}),401

@user_api.route("/api/logout",methods=["POST"])
@login_required
def logout_user_api():
    logout_user()
    return jsonify({"message":"Logged out successfully"}),200

@user_api.route("/api/user",methods=["GET"])
@login_required
def get_current_user():
    return jsonify({"email":current_user.email,"name":current_user.name,"role":current_user.role}),200
