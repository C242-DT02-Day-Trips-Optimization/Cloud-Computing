import os
import json
from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing or invalid!")

# Initialize FastAPI app
app = FastAPI()

def run_clustering_script():
    """
    Executes the clustering script and returns the result as JSON.
    """
    # Path to the clustering script
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "app/main.py"))

    try:
        # Run the clustering script
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )
        # Check for errors in the clustering script
        if result.returncode != 0:
            raise Exception(f"Clustering script error: {result.stderr}")
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clustering script failed: {str(e)}")


@app.post("/distance")
async def calculate_distance(mode: str = "driving"):
    # Run the clustering script
    clustering_result = run_clustering_script()

    # Validate clustering output
    if "grouped_clusters" not in clustering_result:
        raise HTTPException(status_code=500, detail="Invalid clustering output")

    grouped_routes = []

    for cluster in clustering_result["grouped_clusters"]:
        # Origin is the first location in the cluster
        origin = cluster["schedule"][0]["name"]
        # Extract all destinations from the cluster schedule
        destinations = [place["name"] for place in cluster["schedule"]]

        # Determine the final destination and waypoints
        if len(destinations) == 1:
            destination = destinations[0]
            waypoints = ""
        else:
            destination = destinations[-1]
            waypoints = '|'.join(destinations[:-1])

        # Build the Google Directions API URL
        url = (
            f"https://maps.googleapis.com/maps/api/directions/json"
            f"?origin={origin}&destination={destination}&waypoints={waypoints}&mode={mode}&key={GOOGLE_API_KEY}"
        )

        # Make the request to the Google Maps API
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from Google API")

        data = response.json()

        # Validate the API 
        if data["status"] != "OK":
            raise HTTPException(status_code=400, detail=f"Google API Error: {data.get('error_message', 'Unknown error')}")

        # Extract route information
        route = data["routes"][0]
        legs = route["legs"]

        # Build the response
        route_summary = []
        for i, leg in enumerate(legs):
            route_summary.append({
                "start_address": leg["start_address"],
                "end_address": leg["end_address"],
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
                "start_time": cluster["schedule"][i]["start_time"],
                "end_time": cluster["schedule"][i]["end_time"]
            })

        grouped_routes.append({
            "cluster": cluster["cluster"],
            "route": route_summary,
            "total_distance": sum(leg["distance"]["value"] for leg in legs),  # meters
            "total_duration": sum(leg["duration"]["value"] for leg in legs)   # seconds
        })

    final_unvisitable = clustering_result.get("final_unvisitable", [])

    return {
        "grouped_routes": grouped_routes,
        "final_unvisitable": final_unvisitable
    }
