from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id             = db.Column(db.Integer, primary_key=True)
    username       = db.Column(db.String(80), unique=True, nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    password_hash  = db.Column(db.String(255), nullable=False)
    role           = db.Column(db.String(20), nullable=False, default='user')
    department_id  = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)

    # Explicit two-way link to Department
    department     = db.relationship(
        'Department',
        back_populates='users'
    )

    # Tickets this user created
    tickets_created = db.relationship(
        'Ticket',
        back_populates='creator',
        foreign_keys='Ticket.created_by',
        lazy=True
    )
    # Tickets assigned to this user
    tickets_assigned = db.relationship(
        'Ticket',
        back_populates='assignee',
        foreign_keys='Ticket.assigned_to',
        lazy=True
    )

    # Comments this user has made
    comments = db.relationship(
        'Comment',
        back_populates='author',
        lazy=True
    )


class Department(db.Model):
    __tablename__ = 'department'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Explicit two-way link to User
    users = db.relationship(
        'User',
        back_populates='department',
        lazy=True
    )


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(120), nullable=False)
    description  = db.Column(db.Text, nullable=False)
    status       = db.Column(db.String(20), nullable=False, default='Open')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    created_by   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # User who created the ticket
    creator = db.relationship(
        'User',
        back_populates='tickets_created',
        foreign_keys=[created_by]
    )

    # User assigned to the ticket
    assignee = db.relationship(
        'User',
        back_populates='tickets_assigned',
        foreign_keys=[assigned_to]
    )

    comments = db.relationship(
        'Comment',
        back_populates='ticket',
        lazy=True
    )


class Comment(db.Model):
    __tablename__ = 'comment'

    id         = db.Column(db.Integer, primary_key=True)
    ticket_id  = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'),   nullable=False)
    comment    = db.Column(db.Text, nullable=False)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    author     = db.relationship(
        'User',
        back_populates='comments'
    )
    ticket     = db.relationship(
        'Ticket',
        back_populates='comments'
    )
