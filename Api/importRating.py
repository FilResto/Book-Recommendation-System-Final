import pandas as pd
from api import app, db
from api import RatingModel  # Ensure RatingModel is defined in your model

# Display a preview of the first lines of the CSV file
def display_sample_rows(file_path, num_rows=10):
    """Display a preview of the first lines of the CSV file."""
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, nrows=num_rows)
    print(df.head(num_rows))  # Display the first lines of the DataFrame


def clean_userid(userid_str):
    """Clean and validate the user ID."""
    return userid_str.strip() if isinstance(userid_str, str) else None


def clean_bookid(bookid_str):
    """Clean and validate the book ID."""
    return bookid_str.strip() if isinstance(bookid_str, str) else None


def clean_rating(rating_str):
    """Clean and validate the rating."""
    try:
        rating = int(rating_str)
        if 1 <= rating <= 5:
            return rating
        else:
            print(f"Invalid rating (out of range): {rating_str}. Ignored.")
            return None
    except ValueError:
        print(f"Conversion error for rating: {rating_str}. Ignored.")
        return None


def import_ratings():
    # Path to the CSV file containing rating data
    file_path = './data/ratings.csv'

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Display a preview of the first lines to check the data
    print("Preview of the first lines of the CSV file:")
    # display_sample_rows(file_path)

    # List to store RatingModel objects
    ratings = []

    with app.app_context():
        for _, row in df.iterrows():
            # Clean and validate fields
            # user_id = clean_userid(row['userId'])
            user_id = row['userId']
            book_id = clean_bookid(row['bookId'])
            rating = clean_rating(row['rating'])
            print(user_id, book_id, rating)
            if user_id and book_id and rating is not None:
                # Create the RatingModel object
                rating_obj = RatingModel(
                    user_id=user_id,
                    book_id=book_id,
                    rating=rating
                )
                ratings.append(rating_obj)

        # Add ratings to the database
        db.session.add_all(ratings)
        db.session.commit()

    print(f"{len(ratings)} ratings imported successfully!")


# Example usage:
file_path = './data/ratings.csv'

# Import ratings into the database
import_ratings()
