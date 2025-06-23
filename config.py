import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session cookies, CSRF protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Use DATABASE_URL if provided (e.g. by Render), else fall back to SQLite
    uri = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'app.db')}")
    SQLALCHEMY_DATABASE_URI = uri.replace("postgres://", "postgresql://")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
