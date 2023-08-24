import googlemaps
import os
from datetime import datetime
import csv
import uuid

api_key = os.environ.get('MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)

def convert_location_to_geocode(location):
    try:
        result = gmaps.geocode(location)
        if result:
            geometry = result[0].get('geometry', {})
            return geometry.get('location', {})
        else:
            print("Geocode not found for:", location)
            return None

    except googlemaps.exceptions.ApiError as e:
        print("Google Maps API error:", e)
        return None

    except Exception as e:
        print("An error occurred:", e)
        return None


def write_data_to_csv(data_list):
    try:
        output_file = f'{str(uuid.uuid4())}.csv'
        if not data_list:
            print("Data list is empty. Nothing to write to CSV.")
            return None

        field_names = data_list[0].keys()
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)

            writer.writeheader()

            for row in data_list:
                writer.writerow(row)

        print(f"Data successfully written to {output_file}")
        return output_file[:-4]
    except Exception as e:
        print("An error occurred:", e)
        return None

def get_places(location, place_type):
    try:
        geocoded_location = convert_location_to_geocode(location)
        places_raw = gmaps.places_nearby(location=geocoded_location, type=place_type, radius=5000)

        if "results" not in places_raw:
            print("No results found.")
            return []

        places_unfiltered = places_raw['results']
        places = []
        for place in places_unfiltered:
            place_info = {
                "business_status" : place.get("business_status", "N/A"),
                "is_opened": place.get("opening_hours", {}).get("open_now", "N/A"),
                "lat": place["geometry"]["location"].get("lat", "N/A"),
                "lng": place["geometry"]["location"].get("lng", "N/A"),
                "name": place.get("name", "N/A"),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "rating": place.get("rating", "N/A"),
                "place_id": place.get("place_id", "N/A"),
                "place_type": place_type
            }
            places.append(place_info)

        print(f"Number of all places: {len(places)}")
        return places

    except googlemaps.exceptions.ApiError as api_error:
        return {"error": "Google Maps API Error", "message": str(api_error)}

    except KeyError as key_error:
        print("A key error occurred:", key_error)
        return []

    except Exception as e:
        return {"error": "An unexpected error occurred", "message": str(e)}

def get_working_hours(place_id, date):
    try:
        place_details = gmaps.place(place_id)
        if "result" not in place_details:
            print("Place details not found.")
            return False
        opening_hours_data = place_details["result"].get("opening_hours", {}).get("weekday_text", [])
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date_to_check = date_obj.date()
        day_of_week = date_to_check.weekday()
        if opening_hours_data:
            opening_hours_for_day = opening_hours_data[day_of_week]
            print(opening_hours_for_day + place_details["result"]["name"])
            return "Closed" not in opening_hours_for_day
        else:
            print("Opening hours data not available.")
            return False

    except googlemaps.exceptions.ApiError as api_error:
        return {"error": "Google Maps API Error", "message": str(api_error)}

    except Exception as e:
        print("An error occurred:", e)
        return False

def get_directions(location, place_type, date):
    try:
        list_of_places = get_places(location, place_type)
        places_temp = [
            place
            for place in list_of_places
            if place['business_status'] == 'OPERATIONAL'
            and place['rating'] is not None
            and place['user_ratings_total'] > 10
        ]
        print(f"Number of places that are filtered: {len(places_temp)}")

        filtered_places = [
            place for place in places_temp if get_working_hours(place.get('place_id'), date)
        ]
        print(f"Number of places to display: {len(filtered_places)}")

        name_of_csv = {"csv_id": write_data_to_csv(filtered_places)}

        visits = [(place["lat"], place["lng"]) for place in filtered_places]
        waypoints = "|".join([f"{lat},{lng}" for lat, lng in visits])

        directions_result = gmaps.directions(
            origin=location,
            destination=location,
            waypoints=waypoints,
            mode="walking",
            optimize_waypoints=True,
        )
        if directions_result:
            return [filtered_places, directions_result[0], name_of_csv]
        else:
            return {"message": "We could not generate directions"}

    except googlemaps.exceptions.ApiError as api_error:
        return {"error": "Google Maps API Error", "message": str(api_error)}

    except Exception as e:
        return {"error": "An unexpected error occurred", "message": str(e)}

