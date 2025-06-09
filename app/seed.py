import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from . import db
from . models import User, Department
import os
from dotenv import load_dotenv


@click.command('seed')
@with_appcontext
def seed():
    """Seed the database with departments and users."""
    load_dotenv()

    db.drop_all()
    db.create_all()

    # Create departments
    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Support']
    dept_objects = []
    for name in departments:
        d = Department(name=name)
        db.session.add(d)
        dept_objects.append(d)
    db.session.commit()

    # Create admin user
    admin = User(
        username=os.getenv('ADMIN_USERNAME', 'admin'),
        email=os.getenv('ADMIN_EMAIL', 'admin@example.com'),
        password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'ChangeMe123!')),
        role='admin',
        department_id=dept_objects[0].id
    )
    db.session.add(admin)

    # Create 19 regular users across departments
    for i in range(1, 20):
        user = User(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password_hash=generate_password_hash('password123'),
            role='user',
            department_id=dept_objects[i % len(dept_objects)].id
        )
        db.session.add(user)

    db.session.commit()
    print("Database seeded successfully.")


def register_commands(app):
    app.cli.add_command(seed)
