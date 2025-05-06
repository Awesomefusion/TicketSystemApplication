from flask import Blueprint, render_template, redirect, url_for, flash, request
from .. import db, login_manager
from ..models import User
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return "Login Page Placeholder"

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
