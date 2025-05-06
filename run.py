from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # make sure all tables are created
    with app.app_context():
        db.create_all()
        print("🔧  Initialized database and tables.")
    app.run(debug=True)
