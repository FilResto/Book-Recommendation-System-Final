import pandas as pd
from api import app, db
from api import UserModel
import json
from werkzeug.security import generate_password_hash, check_password_hash

def import_data():
    # Load the raw CSV file
    file_path = './data/users.csv'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Remove the header
    data_lines = lines[1:]

    # Split each line and convert to UserModel objects
    users = []
    for line in data_lines:
        line = line.strip()  # Supprimer les espaces ou sauts de ligne
        values = line.split(',', maxsplit=4)  # Découper en 4 parties : idd, age, email, generi_preferiti
        
        # Assign values and clean if necessary
        id = int(values[0].strip('"'))
        idd = int(values[1].strip('"'))  
        age = int(values[2].strip('"'))  
        email = values[3].strip('"') 
        generi_preferiti = values[4].strip('"')  

        # Clean and serialize preferred genres
        generi_preferiti = json.dumps(generi_preferiti.split(';'))  # Si les genres sont séparés par ";"

        # Create a user with a default hashed password
        user = UserModel(
            id=id,
            idd=idd,
            age=age,
            email=email,
            password_hash=generate_password_hash("password123"),  # Mot de passe par défaut
            generi_preferiti=generi_preferiti
        )
        users.append(user)

    # Add users to the database
    with app.app_context():
        db.session.add_all(users)
        db.session.commit()

    print("Data imported successfully!")

# Execute data import
import_data()