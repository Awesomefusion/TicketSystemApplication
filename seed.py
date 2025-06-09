import os
import random
from faker import Faker
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, Department
from dotenv import load_dotenv

load_dotenv()
app = create_app()
fake = Faker()

# Load admin credentials from .env
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Predefined departments
departments = ['Engineering', 'Support', 'Marketing', 'Sales', 'HR']

@app.cli.command("seed")
def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Add departments
        dept_objs = []
        for name in departments:
            d = Department(name=name)
            db.session.add(d)
            dept_objs.append(d)
        db.session.commit()
        print("Departments added.")

        # Add admin
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            role='admin',
            department=random.choice(dept_objs)
        )
        db.session.add(admin)

        # Add 19 regular users
        for i in range(1, 20):
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password_hash=generate_password_hash("Userpass123"),
                role='user',
                department=random.choice(dept_objs)
            )
            db.session.add(user)

        db.session.commit()
        print("Admin and 19 users added.")
