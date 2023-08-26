from datetime import datetime
from get_data import get_places, get_directions
from filters import sort_places_by_ratings, sort_places_by_working_hours
from helpers import transform_places


def generate_locations(location, place_type):
    try:
        list_of_locations = get_places(location, place_type)
        return transform_places(list_of_locations)
    except Exception as e:
        print("An error occurred:", e)
        return []

def generate_directions(location, place_type, date):
    try:
        list_of_places = generate_locations(location, place_type)
        sorted_places = sort_places_by_ratings(list_of_places)
        print(f"Number of places that are filtered: {len(sorted_places)}")
        filtered_places = sort_places_by_working_hours(sorted_places, date)
        print(f"Number of places to display: {len(filtered_places)}")
        locations_data_set = {
            "date": datetime.now(),
            "start_location": location,
            "locations": filtered_places
        }
        visits = [(place["lat"], place["lng"]) for place in filtered_places]
        waypoints = "|".join([f"{lat},{lng}" for lat, lng in visits])
        directions_result = get_directions(location, waypoints)
        if directions_result:
            return [filtered_places, directions_result, locations_data_set]
        else:
            return {"message": "We could not generate directions"}
    except Exception as e:
        return {"error": "An error occurred", "message": str(e)}