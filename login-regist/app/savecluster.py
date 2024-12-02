from flask import Flask, request, jsonify
from google.cloud import firestore
from datetime import datetime
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, initialize_app

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

# Initialize Flask app
app = Flask(__name__)

# Endpoint untuk menyimpan data cluster
@app.route('/api/save_cluster/<user_id>', methods=['POST'])
def save_cluster(user_id):
    try:
        # Parse incoming JSON data
        data = request.json
        grouped_clusters = data.get('grouped_clusters')

        # Validasi input
        if not grouped_clusters:
            return jsonify({"error": "No cluster data provided"}), 400
        
        # Menyimpan data cluster ke Firestore
        cluster_ref = db.collection('user_clusters').document(user_id)
        cluster_ref.set({
            "user_id": user_id,
            "grouped_clusters": grouped_clusters,
            "timestamp": datetime.utcnow().isoformat()  # Menyimpan timestamp UTC
        })

        return jsonify({"message": "Cluster data saved successfully"}), 200

    except Exception as e:
        print(f"Error saving cluster: {e}")
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8001)
