from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth, initialize_app
from google.cloud import firestore
from datetime import datetime
import bcrypt
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    initialize_app(cred, {
        'projectId': 'day-trip-optimization'  # Replace with your Firebase project ID
    })

# Initialize Firestore client
db = firestore.Client(project='day-trip-optimization', database='daytripdb')

# Initialize Blueprint
user_bp = Blueprint('user', __name__)

# Helper function to hash passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# User registration (Create)
@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not all([email, username, password, confirm_password]):
            return jsonify({"error": "All fields are required"}), 400
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Create user in Firebase Auth
        user = auth.create_user(email=email, password=password)

        # Save user data (including hashed password) to Firestore
        db.collection('users').document(user.uid).set({
            "username": username,
            "email": email,
            "password": hashed_password.decode('utf-8'),  # Store the hashed password as a string
            "created_at": datetime.utcnow().isoformat()
        })

        return jsonify({"message": "User registered successfully", "uid": user.uid}), 201
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error": str(e)}), 500

# User login (Read)
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        identifier = data.get('identifier')  # Can be username or email
        password = data.get('password')

        if not identifier or not password:
            return jsonify({"error": "Identifier and password are required"}), 400

        # Determine if identifier is email or username
        if '@' in identifier:
            email = identifier
        else:
            username = identifier.lower()
            user_doc = db.collection('users').where('username', '==', username).get()
            if not user_doc:
                return jsonify({"error": "Username not found"}), 404
            email = user_doc[0].to_dict().get('email')

        # Use Firebase REST API to log in
        firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}"
        response = requests.post(firebase_url, json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        })

        if response.status_code == 200:
            user_data = response.json()
            return jsonify({
                "message": "Login successful",
                "idToken": user_data["idToken"],
                "refreshToken": user_data["refreshToken"],
                "expiresIn": user_data["expiresIn"],
                "userId": user_data["localId"]
            }), 200
        else:
            return jsonify({"error": response.json().get("error", {}).get("message", "Login failed")}), 400

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": str(e)}), 500


# Update user details (Update)
@user_bp.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')  # Password to update (hashed)

        if not username and not email and not password:
            return jsonify({"error": "At least one field must be provided to update"}), 400

        user_ref = db.collection('users').document(user_id)
        
        # Prepare update data
        update_data = {}
        if username:
            update_data['username'] = username
        if email:
            update_data['email'] = email
        if password:
            update_data['password'] = hash_password(password).decode('utf-8')  # Hash the new password
        
        if update_data:
            update_data['updated_at'] = datetime.utcnow().isoformat()
            user_ref.update(update_data)

        # After updating, fetch the updated data and return it with 'email' before 'username'
        updated_user = user_ref.get()
        if updated_user.exists:
            updated_data = updated_user.to_dict()
            # Ensure email comes first and username comes below it
            ordered_data = {
                "email": updated_data.get("email"),
                "username": updated_data.get("username"),
                "password": updated_data.get("password"),
                "created_at": updated_data.get("created_at"),
                "updated_at": updated_data.get("updated_at")
            }
            return jsonify({"message": "User updated successfully", "user": ordered_data}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": str(e)}), 500


# Get user details (Read)
@user_bp.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_ref = db.collection('users').document(user_id)
        user_data = user_ref.get()

        if user_data.exists:
            user_dict = user_data.to_dict()
            ordered_data = {
                "email": user_dict.get("email"),
                "username": user_dict.get("username"),
                "password": user_dict.get("password"),
                "created_at": user_dict.get("created_at"),
                "updated_at": user_dict.get("updated_at")
            }
            return jsonify(ordered_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error reading user: {e}")
        return jsonify({"error": str(e)}), 500


# Delete user (Delete)
@user_bp.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_ref = db.collection('users').document(user_id)
        user_ref.delete()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({"error": str(e)}), 500
