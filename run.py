import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

# Predefined admin credentials (override via environment variables if desired)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'ChangeMe123!')

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        print("🔧  Initialized database and tables.")

        # Ensure admin user exists
        admin = User.query.filter_by(username=ADMIN_USERNAME).first()
        if admin:
            print(f"👤 Admin user '{ADMIN_USERNAME}' already exists.")
        else:
            hashed_pw = generate_password_hash(ADMIN_PASSWORD)
            admin = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password_hash=hashed_pw,
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print(
                f"✅ Admin user '{ADMIN_USERNAME}' created with default password."
            )

    # Run the Flask development server
    app.run(debug=True)
