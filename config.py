import os
from pathlib import Path

basedir = Path(__file__).parent.resolve()

class Config:
    # Secret key for session cookies, CSRF protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Grab DATABASE_URL if set (e.g. on Heroku/Render), else fall back to SQLite
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # SQLAlchemy 1.x wants "postgresql://", not "postgres://"
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    else:
        db_url = f"sqlite:///{basedir / 'app.db'}"

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
