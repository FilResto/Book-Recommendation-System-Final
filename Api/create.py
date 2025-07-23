from api import app, db  # Make sure db is properly imported

# Create tables in the database
with app.app_context():
    db.create_all()
