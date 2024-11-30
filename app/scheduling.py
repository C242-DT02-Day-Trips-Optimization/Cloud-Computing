from geopy.distance import geodesic
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import googlemaps
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

def get_travel_time(start_coords, end_coords, distance_threshold=1.0):
    """
    Get travel time between two locations using Google Maps API.
    """
    distance = geodesic(start_coords, end_coords).kilometers
    mode = "walking" if distance <= distance_threshold else "driving"

    # Fetch travel time using Google Maps API
    directions = gmaps.directions(
        origin=start_coords,
        destination=end_coords,
        mode=mode,
        departure_time=datetime.now()
    )

    if directions:
        duration = directions[0]['legs'][0]['duration']['value'] / 60  # Convert seconds to minutes
        return round(duration), mode
    else:
        return 0, mode


def calculate_total_time_in_minutes(daily_start_time, daily_end_time):
    """
    Calculate total available time in minutes based on start and end times.
    """
    start_time = datetime.strptime(daily_start_time, "%H:%M")
    end_time = datetime.strptime(daily_end_time, "%H:%M")
    total_time = (end_time - start_time).seconds / 60  # Convert seconds to minutes
    return total_time


def calculate_average_duration(total_time, num_locations):
    """
    Calculate the average time allocated for each location within a cluster.
    """
    if num_locations == 0:
        return 0
    return total_time / num_locations


def create_schedule_entry(location, avg_duration=None, travel_time=None, mode=None):
    """
    Create a schedule entry with proximity, travel time, and mode details.
    """
    entry = {
        "name": location.name,
        "coordinates": location.coordinates,
        "avg_duration": avg_duration,
        "travel_time": travel_time,
        "mode": mode,
    }
    return entry


def handle_unvisitable(locations, clusters):
    """
    Handle unvisitable locations and try to fit them into other clusters.
    Locations that cannot fit into any cluster will be returned as 'unvisitable'.
    """
    new_unvisitable = []
    
    for location in locations:
        fit = False
        
        for cluster_id, cluster_schedule in clusters.items():
            # Attempt to schedule this location in the cluster, based on available time
            result = schedule_single_location(location, cluster_schedule["schedule"], avg_duration=cluster_schedule["avg_duration"])
            
            if result:
                cluster_schedule["schedule"].append(result)
                cluster_schedule["schedule"].sort(key=lambda x: x["proximity_to_next"])  # Sort based on proximity to the next
                fit = True
                break
        
        if not fit:
            # If the location couldn't fit in any cluster, add it to the 'unvisitable' list
            new_unvisitable.append(location)
    
    return {"clusters": clusters, "unvisitable": new_unvisitable}


def schedule_single_location(location, current_schedule, avg_duration=None):
    """
    Schedule a single location within a cluster, purely based on proximity and average duration.
    """
    if not current_schedule:
        # No locations scheduled yet, schedule the first one
        return create_schedule_entry(location, avg_duration=avg_duration)

    last_location = current_schedule[-1]
    distance_to_last = geodesic(last_location["coordinates"], location.coordinates).kilometers
    return create_schedule_entry(location, proximity_to_last=distance_to_last, avg_duration=avg_duration)


def schedule_cluster_with_proximity(cluster, daily_start_time_str, daily_end_time_str):
    """
    Schedule locations within a cluster based on proximity and travel time.
    """
    schedule = []
    unvisitable = []
    total_distance = 0  # Initialize total distance
    total_travel_time = 0  # Initialize total travel time

    # Calculate total available time
    total_available_time = calculate_total_time_in_minutes(daily_start_time_str, daily_end_time_str)
    total_locations = len(cluster)

    # Calculate total travel time and distance
    for i in range(len(cluster) - 1):
        travel_time, _ = get_travel_time(cluster[i].coordinates, cluster[i + 1].coordinates)
        distance = geodesic(cluster[i].coordinates, cluster[i + 1].coordinates).kilometers
        total_travel_time += travel_time
        total_distance += distance

    # Remaining time for activities (exclude travel time)
    time_for_activities = total_available_time - total_travel_time
    if time_for_activities <= 0:
        return {
            "schedule": [],
            "unvisitable": cluster,
            "total_distance": total_distance,
            "total_travel_time": total_travel_time
        }

    avg_duration = calculate_average_duration(time_for_activities, total_locations)

    # Start scheduling
    if cluster:
        first_location = cluster[0]
        schedule.append(create_schedule_entry(first_location, avg_duration=avg_duration))
        cluster.pop(0)

    while cluster:
        last_location = schedule[-1]
        next_location = min(cluster, key=lambda loc: geodesic(last_location["coordinates"], loc.coordinates).kilometers)
        cluster.remove(next_location)

        travel_time, mode = get_travel_time(last_location["coordinates"], next_location.coordinates)
        distance = geodesic(last_location["coordinates"], next_location.coordinates).kilometers
        total_distance += distance
        schedule_entry = create_schedule_entry(next_location, avg_duration, travel_time, mode)
        if schedule_entry:
            schedule.append(schedule_entry)
        else:
            unvisitable.append(next_location)

    # Add proximity details to the schedule
    for i in range(len(schedule) - 1):
        distance_to_next = geodesic(schedule[i]["coordinates"], schedule[i + 1]["coordinates"]).kilometers
        schedule[i]["proximity_to_next"] = f"{distance_to_next:.2f} km"

    if schedule:
        schedule[-1]["proximity_to_next"] = "N/A"  # Last location has no next

    return {
        "schedule": schedule,
        "unvisitable": unvisitable,
        "total_distance": total_distance,
        "total_travel_time": total_travel_time,
        "avg_duration_per_location": avg_duration
    }


def parallel_schedule_clusters(clusters, daily_start_time, daily_end_time, num_threads=4):
    """
    Schedules multiple clusters in parallel using multithreading.
    """
    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {
            cluster_id: executor.submit(
                schedule_cluster_with_proximity,
                cluster_locations,
                daily_start_time,
                daily_end_time,
            )
            for cluster_id, cluster_locations in clusters.items()
        }

        for cluster_id, future in futures.items():
            cluster_data = future.result()

            # Handle unvisitable locations
            result = handle_unvisitable(cluster_data["unvisitable"], clusters)

            # Add results for each cluster
            results.append({
                "cluster": cluster_id,
                "schedule": cluster_data["schedule"],
                "total_duration": round(cluster_data["total_travel_time"] + len(cluster_data["schedule"]) * cluster_data["avg_duration_per_location"], 2),
                "avg_duration": cluster_data["avg_duration_per_location"],
                "total_travel_time": cluster_data["total_travel_time"],
                "total_distance": round(cluster_data["total_distance"], 2),
                "unvisitable": result["unvisitable"],
            })

    return results


