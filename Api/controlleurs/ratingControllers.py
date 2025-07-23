from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from backend.app.models.rating import Rating
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()
# Configure the database connection
DATABASE_URL = 'sqlite:///library.db'  # Replace with your database URL
engine = create_engine(DATABASE_URL)
Rating.metadata.create_all(engine)  # Create tables if they do not exist yet
Session = sessionmaker(bind=engine)

def load_visualisation_from_csv(file_path):
    # Create a new session
    session = Session()
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert each row to a Book object and add it to the session
    for _, row in df.iterrows():
        rating = Rating(
            user_id=row['userId'],
            book_id=row['bookId'],
            rating=row['rating']
        )
        session.add(rating)

    # Commit and close the session
    session.commit()
    session.close()


def findAll():
    ratings = Rating.query.all()
    return jsonify([rating.to_dict() for rating in ratings])

