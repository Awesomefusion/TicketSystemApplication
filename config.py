import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    uri = os.environ.get('DATABASE_URL',
                         f"sqlite:///{os.path.join(basedir, 'app.db')}")
    # Heroku hands you a postgres:// URL, but SQLAlchemy wants postgresql://
    SQLALCHEMY_DATABASE_URI = uri.replace("postgres://", "postgresql://")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # force SSL on Postgres
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "sslmode": "require"
        }
    }
