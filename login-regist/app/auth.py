from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import auth, credentials, firestore, initialize_app
from datetime import datetime


# Inisialisasi Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    initialize_app(cred)

# Inisialisasi Firestore
db = firestore.Client()

# Deklarasi API Key
api_key = "AIzaSyAUxJ1IKE8kDiudpz_lBTAsiwf2lF8FW4Y"


# Define Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return "Auth Blueprint Home"

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Validasi input
    if not all([email, username, password, confirm_password]):
        return jsonify({"error": "All fields (email, username, password, confirm_password) are required"}), 400
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400
    if ' ' in username or not username.isalnum():
        return jsonify({"error": "Username must be alphanumeric and cannot contain spaces"}), 400


    try:
        # Cek apakah username sudah digunakan
        username = username.lower()
        existing_user = db.collection('users').where('username', '==', username).get()
        if len(existing_user) > 0:
            return jsonify({"error": "Username is already taken"}), 400

        # Buat pengguna di Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )

        # Simpan username dan email di Firestore
        db.collection('users').document(user.uid).set({
            "username": username,
            "email": email,
            "created_at": datetime.utcnow().isoformat()
        })

        return jsonify({"message": "User registered successfully", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')  # Bisa username atau email
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"error": "Identifier (email/username) and password are required"}), 400

    try:
        # Identifikasi apakah input adalah email atau username
        if '@' in identifier:  # Asumsikan email jika mengandung '@'
            email = identifier
        else:
            username = identifier.lower()
            user_doc = db.collection('users').where('username', '==', identifier).get()
            if len(user_doc) == 0:
                return jsonify({"error": "Username not found"}), 404
            email = user_doc[0].to_dict().get('email')

        # Login menggunakan Firebase Authentication REST API
        import requests

        firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        
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
        return jsonify({"error": str(e)}), 500


