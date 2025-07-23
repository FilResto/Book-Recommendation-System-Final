from flask import request, jsonify
from flask_jwt_extended import create_access_token

from backend.app.models.user import User


def login():
    # Get the request data
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check that the user exists
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create a JWT token for the user
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200