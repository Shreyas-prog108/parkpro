from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime,timezone

db=SQLAlchemy()

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(150),nullable=False)
    role=db.Column(db.String(10),default="user")
    reservations=db.relationship('Reservation',backref='user',cascade="all,delete-orphan")
    pincode=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(255),nullable=False)
    vehicles=db.relationship('Vehicle',backref='user',cascade="all,delete-orphan")

class Vehicle(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    number=db.Column(db.String(20),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    reservations=db.relationship('Reservation',backref='vehicle',cascade="all,delete-orphan")

class Parkinglot(db.Model):
    id=db.Column(db.Integer,unique=True,primary_key=True)
    prime_location_name=db.Column(db.String(255),nullable=False)
    price_per_hour=db.Column(db.Float,nullable=False)
    address=db.Column(db.String(255),nullable=False)
    pin_code=db.Column(db.Integer,nullable=False)
    number_of_spots=db.Column(db.Integer,nullable=False)
    spots=db.relationship('Spot',backref='lot',cascade="all,delete-orphan")

class Spot(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    status=db.Column(db.String(20),nullable=False,default='A')
    lot_id=db.Column(db.Integer,db.ForeignKey('parkinglot.id'),nullable=False)
    reservations=db.relationship('Reservation',backref='spot',cascade="all,delete-orphan")

class Reservation(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    spot_id=db.Column(db.Integer,db.ForeignKey('spot.id'),nullable=False)
    vehicle_id=db.Column(db.Integer,db.ForeignKey('vehicle.id'),nullable=True)
    parking_timestamp=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    leaving_timestamp=db.Column(db.DateTime,nullable=True)
    parking_cost=db.Column(db.Float,nullable=False,default=0.0)
