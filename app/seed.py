import os
import random
import click
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from . import db
from .models import User, Department, Ticket

seed_cli = AppGroup('seed')


@seed_cli.command('all')
def seed_all():
    """Seed departments, users and tickets."""
    seed_departments()
    seed_users()
    seed_tickets()
    click.echo('Database seeding complete.')


def seed_departments():
    dept_names = ['IT Support', 'Human Resources', 'Finance', 'Operations', 'Marketing']
    for name in dept_names:
        if not Department.query.filter_by(name=name).first():
            db.session.add(Department(name=name))
    db.session.commit()
    click.echo('  • Departments seeded.')


def seed_users():
    # Admin from env (fallbacks)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'ChangeMe123!')

    # Create admin if missing
    if not User.query.filter_by(username=ADMIN_USERNAME).first():
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            role='admin'
        )
        db.session.add(admin)
        click.echo(f'  • Admin "{ADMIN_USERNAME}" created.')

    # Grab departments for assignment
    departments = Department.query.all()

    # Create 9 normal users
    for i in range(1, 10):
        username = f'user{i}'
        email = f'user{i}@example.com'
        if not User.query.filter_by(username=username).first():
            # round-robin department assignment
            dept = departments[(i - 1) % len(departments)]
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash('userpass'),
                role='user',
                department_id=dept.id
            )
            db.session.add(user)
    db.session.commit()
    click.echo('  • 9 normal users seeded.')


def seed_tickets():
    normal_users = User.query.filter_by(role='user').all()
    if not normal_users:
        click.echo('No normal users found—run users seed first.')
        return

    sample_tickets = [
        {'title': 'VPN Connectivity Issues',     'description': 'Cannot connect to VPN from home network.'},
        {'title': 'Email Delivery Failure',      'description': 'Emails to external domain bounce back with error code 550.'},
        {'title': 'Software Installation Request','description': 'Need Microsoft Visio installed on my workstation.'},
        {'title': 'Password Reset Needed',       'description': 'Forgot corporate password and cannot login.'},
        {'title': 'ERP System Slowdown',         'description': 'Finance ERP taking too long to load reports.'},
        {'title': 'Payroll Mismatch',            'description': 'Salary for July shows incorrect amount.'},
        {'title': 'Leave Balance Discrepancy',   'description': 'Annual leave balance is showing negative days.'},
        {'title': 'Printer Network Error',       'description': 'Office printer on Floor 2 shows offline.'},
        {'title': 'Conference Room Booking Error','description': 'Cannot book meeting room via portal.'},
        {'title': 'Broken Desk Phone',           'description': 'No dial tone on desk phone.'},
        {'title': 'Air Conditioning Issue',      'description': 'AC unit in main lobby not cooling.'},
        {'title': 'Browser Crash',               'description': 'Browser crashes when accessing intranet site.'},
        {'title': 'Access Denied Error',         'description': 'Denied access to shared HR drive.'},
        {'title': 'Invoice Submission Failure',  'description': 'Unable to upload invoice PDF to finance portal.'},
        {'title': 'Keyboard Malfunction',        'description': 'Numeric keypad keys are not responding.'},
    ]

    statuses = ['Open', 'In Progress', 'Closed']

    for item in sample_tickets:
        creator = random.choice(normal_users)
        assignee = random.choice(normal_users)
        ticket = Ticket(
            title=item['title'],
            description=item['description'],
            status=random.choice(statuses),
            created_by=creator.id,
            assigned_to=assignee.id
        )
        db.session.add(ticket)

    db.session.commit()
    click.echo('  • 15 tickets seeded.')


def register_commands(app):
    app.cli.add_command(seed_cli)
