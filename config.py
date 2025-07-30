import os,secrets

BASE_DIR=os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR=os.path.join(BASE_DIR, "instance")

if not os.path.exists(INSTANCE_DIR):
    os.makedirs(INSTANCE_DIR)

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY", secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'parking_details.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SESSION_TYPE="filesystem"
