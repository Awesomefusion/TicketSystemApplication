from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Department
from ..forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tickets.list_tickets'))

    form = LoginForm()
    next_page = request.args.get('next')
    if form.validate_on_submit():
        ident = form.identifier.data
        user = User.query.filter(
            or_(User.email == ident, User.username == ident)
        ).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(next_page or url_for('tickets.list_tickets'))
        flash('Invalid credentials', 'error')
    return render_template('login.html', form=form, next=next_page)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pw,
            department_id=form.department_id.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You may now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
