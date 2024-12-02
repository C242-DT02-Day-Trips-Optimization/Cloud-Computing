from flask import Flask, jsonify
from google.cloud import firestore
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

# Endpoint untuk membaca data cluster berdasarkan user_id
@app.route('/api/get_cluster/<user_id>', methods=['GET'])
def get_cluster(user_id):
    try:
        # Mendapatkan data cluster berdasarkan user_id
        cluster_ref = db.collection('user_clusters').document(user_id)
        cluster_data = cluster_ref.get()

        if cluster_data.exists:
            return jsonify(cluster_data.to_dict()), 200
        else:
            return jsonify({"error": "Cluster not found"}), 404

    except Exception as e:
        print(f"Error reading cluster: {e}")
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8002)
