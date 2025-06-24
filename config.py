import os
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Pull from DATABASE_URL (Heroku) or fallback to SQLite locally
    uri = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    )

    # sqlalchemy wants postgresql:// not postgres://
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
