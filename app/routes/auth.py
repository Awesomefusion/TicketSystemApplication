from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Department
from ..forms import LoginForm, RegistrationForm

# no template_folder override here—let Flask use app/templates/
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tickets.dashboard'))

    form = LoginForm()
    next_page = request.args.get('next') or url_for('tickets.list_tickets')

    if form.validate_on_submit():
        ident = form.identifier.data
        user = User.query.filter(
            or_(User.email == ident, User.username == ident)
        ).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(next_page)

        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form, next=next_page)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # populate the dropdown every time
    form.department_id.choices = [
        (d.id, d.name) for d in Department.query.order_by(Department.name)
    ]

    if form.validate_on_submit():
        # double-check no duplicate
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'error')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
        else:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                department_id=form.department_id.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You may now log in.', 'success')
            return redirect(url_for('auth.login'))

    # either GET or validation failed
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
