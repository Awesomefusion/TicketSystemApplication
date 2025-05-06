import os

# project root directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ticket_system.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
