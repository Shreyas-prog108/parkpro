from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from models import db, User

admin_api=Blueprint("admin_api", __name__)

@admin_api.route("/api/login",methods=["POST"])
def login_user_api():
    data=request.get_json()    
    if not data or not all(k in data for k in ["email", "password"]):
        return jsonify({"error": "Missing email or password"}),400    
    user=User.query.filter_by(email=data["email"]).first()    
    if user and user.role=='admin' and check_password_hash(user.password, data["password"]):
        login_user(user)
        return jsonify({"message": "Login successful"}),200    
    return jsonify({"error": "Invalid credentials"}),401

@admin_api.route("/api/logout",methods=["POST"])
@login_required
def logout_user_api():
    if current_user.role!='admin':
        return jsonify({"error":"Unauthorized"}),403
    logout_user()
    return jsonify({"message":"Logged out successfully"}),200

@admin_api.route("/api/user",methods=["GET"])
@login_required
def get_current_user():
    if current_user.role!='admin':
        return jsonify({"error":"Unauthorized"}),403
    return jsonify({"email":current_user.email,"name":current_user.name,"role":current_user.role}),200


