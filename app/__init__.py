from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # initialise extensions
    db.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from .routes.auth import auth_bp
    from .routes.tickets import tickets_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)

    # root redirect
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    # health check endpoint
    @app.route('/health')
    def health():
        return 'OK', 200

    # custom error pages
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    with app.app_context():
        db.create_all()

    return app
