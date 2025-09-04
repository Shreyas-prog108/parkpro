import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# if not os.path.exists(INSTANCE_DIR):
#     os.makedirs(INSTANCE_DIR)

def get_database_uri():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        db_url = db_url.strip()
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        if db_url:
            return db_url
    return f"sqlite:///parking_details.db"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_DIR, 'parking_details.db')}"

class ProductionConfig(Config):
    DEBUG = False  # ✅ Security: Disable debug in production
    SQLALCHEMY_DATABASE_URI = get_database_uri()

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
