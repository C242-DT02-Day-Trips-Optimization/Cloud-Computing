import httpx
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def fetch_place_by_name(place_name: str):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": place_name,
        "key": GOOGLE_MAPS_API_KEY,
    }

    response = httpx.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

def process_place_data(data: dict) -> pd.DataFrame:
    places = []
    for place in data.get("results", []):
        places.append({
            "Title": place.get("name"),
            "Address": place.get("formatted_address"),
            "Reviews": place.get("user_ratings_total", 0),
            "Rating": place.get("rating", 0.0),
            "Latitude": place["geometry"]["location"]["lat"],
            "Longitude": place["geometry"]["location"]["lng"],
        })
    return pd.DataFrame(places)

def main():
    if not GOOGLE_MAPS_API_KEY:
        print("Error: Please set your GOOGLE_MAPS_API_KEY in the .env file.")
        return

    place_name = input("Enter the name of the tourist attraction: ")

    try:
        print(f"Searching for '{place_name}'...")
        data = fetch_place_by_name(place_name)
        df = process_place_data(data)

        if df.empty:
            print(f"No results found for '{place_name}'.")
        else:
            output_file = "tourist_place_details.csv"
            df.to_csv(output_file, index=False)
            print(f"Details of '{place_name}' saved to {output_file}")
            print(df)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
