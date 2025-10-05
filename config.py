import os
import secrets
from urllib.parse import urlparse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_database_uri():
    """
    Returns the database URI.
    Prioritizes Neon pooled connection URL if set in environment variable DATABASE_URL.
    Falls back to SQLite if not provided.
    """
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        db_url = db_url.strip()
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return db_url
    # return f"sqlite:///{os.path.join(BASE_DIR, 'parking_details.db')}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    
    # Neon serverless
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 5,           
        "max_overflow": 2,        
        "pool_pre_ping": True,    
        "pool_recycle": 280      
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False 


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
