import pandas as pd
from api import app, db
from api import GenreModel


def import_genre():
    # Load the raw CSV file
    file_path = './data/genres.csv'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Remove the header
    data_lines = lines[1:]

    # Split each line and convert to genreModel objects
    genres = []
    for line in data_lines:
        line = line.strip()  # Supprimer les espaces ou sauts de ligne
        values = line.split(',', maxsplit=1)  # Découper en 1 parties : idd, age, email, generi_preferiti
        
        # Assign values and clean if necessary
        id = int(values[0].strip('"')) 
        name = values[1].strip('"')  


        # Create a genre
        genre = GenreModel(
            id=id,
            name=name,
        )
        genres.append(genre)

    # Add genres to the database
    with app.app_context():
        db.session.add_all(genres)
        db.session.commit()

    print("Data imported successfully!")

# Execute data import
import_genre()