import pytest
from app import create_app, db
from app.models import User, Ticket, Comment, Department
from werkzeug.security import generate_password_hash

@pytest.fixture
def app(monkeypatch):
    # Ensure SECRET_KEY is set for testing
    monkeypatch.setenv('SECRET_KEY', 'test-secret-key')

    # Create a Flask app configured for testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        # Cleanup: drop all tables
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    # Create department for admin (IT Support)
    dept = Department(name="IT Support")
    db.session.add(dept)
    db.session.commit()

    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=generate_password_hash("adminpass"),
        role="admin",
        department_id=dept.id
    )
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def normal_user(app):
    # Create department for normal user (Sales)
    dept = Department(name="Sales")
    db.session.add(dept)
    db.session.commit()

    user = User(
        username="testuser",
        email="user@example.com",
        password_hash=generate_password_hash("userpass"),
        role="user",
        department_id=dept.id
    )
    db.session.add(user)
    db.session.commit()
    return user
