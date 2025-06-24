import os
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # keep using a default for local dev
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # pick up Heroku’s DATABASE_URL (or fall back to SQLite locally)
    uri = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )

    # Heroku hands you a postgres:// URL, but SQLAlchemy wants postgresql://
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    # force SSL on Postgres connections
    if uri.startswith("postgresql://") and "sslmode" not in uri:
        uri = uri + "?sslmode=require"

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
