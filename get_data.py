import googlemaps
import os

api_key = os.environ.get("MAPS_API_KEY")
gmaps = googlemaps.Client(key=api_key)


def convert_location_to_geocode(location):
    try:
        result = gmaps.geocode(location)
        if result:
            geometry = result[0].get("geometry", {})
            return geometry.get("location", {})
        else:
            print("Geocode not found for:", location)
            return None

    except googlemaps.exceptions.ApiError as e:
        print("Google Maps API error:", e)
        return None

    except Exception as e:
        print("An error occurred:", e)
        return None


def get_places(location, place_type):
    try:
        geocoded_location = convert_location_to_geocode(location)
        places_raw = gmaps.places_nearby(
            location=geocoded_location, type=place_type, radius=5000
        )

        if "results" not in places_raw:
            print("No results found.")
            return []
        return places_raw["results"]

    except googlemaps.exceptions.ApiError as api_error:
        return {"error": "Google Maps API Error", "message": str(api_error)}

    except Exception as e:
        return {"error": "An unexpected error occurred", "message": str(e)}


def get_place_details(place_id):
    try:
        place_details = gmaps.place(place_id)
        if "result" not in place_details:
            print("Place details not found.")
            return False
        return place_details

    except googlemaps.exceptions.ApiError as api_error:
        return {"error": "Google Maps API Error", "message": str(api_error)}

    except Exception as e:
        print("An error occurred:", e)
        return False


def get_directions(location, waypoints):
    try:
        directions_result = gmaps.directions(
            origin=location,
            destination=location,
            waypoints=waypoints,
            mode="walking",
            optimize_waypoints=True,
        )
        if directions_result:
            return directions_result[0]
        else:
            return {"message": "We could not generate directions"}

    except googlemaps.exceptions.ApiError as api_error:
        return {"error": "Google Maps API Error", "message": str(api_error)}

    except Exception as e:
        return {"error": "An unexpected error occurred", "message": str(e)}
