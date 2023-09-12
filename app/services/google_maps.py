import os
import datetime
from googlemaps import Client
from app.db.crud import insert_data
from app.utils.logger import logger

api_key = os.environ.get("GOOGLE_MAPS_API_KEY")


class GoogleMapsAPI:
    def __init__(self, api_key):
        self.client = Client(api_key)

    def get_places(self, location, place_type):
        try:
            geocoded_location = self.convert_location_to_geocode(location)
            places_raw = self.client.places_nearby(
                location=geocoded_location, type=place_type, radius=5000
            )

            if "results" not in places_raw:
                print("No results found.")
                return []
            insert_data(
                {"timestamp": datetime.datetime.now(), "function": "places_nearby"},
                collection="statistics",
            )
            return places_raw["results"]

        except self.client.exceptions.ApiError as api_error:
            return {"error": "Google Maps API Error", "message": str(api_error)}

        except Exception as e:
            return {"error": "An unexpected error occurred", "message": str(e)}

    def convert_location_to_geocode(self, location):
        try:
            result = self.client.geocode(location)
            if result:
                geometry = result[0].get("geometry", {})
                insert_data(
                    {"timestamp": datetime.datetime.now(), "function": "geocode"},
                    collection="statistics",
                )
                return geometry.get("location", {})
            else:
                print("Geocode not found for:", location)
                return None

        except self.client.exceptions.ApiError as e:
            print("Google Maps API error:", e)
            return None

        except Exception as e:
            print("An error occurred:", e)
            return None

    def get_place_details(self, place_id):
        try:
            place_details = self.client.place(place_id)
            if "result" not in place_details:
                print("Place details not found.")
                return False
            insert_data(
                {"timestamp": datetime.datetime.now(), "function": "place_details"},
                collection="statistics",
            )
            return place_details

        except self.client.exceptions.ApiError as api_error:
            return {"error": "Google Maps API Error", "message": str(api_error)}

        except Exception as e:
            print("An error occurred:", e)
            return False

    def get_directions(self, location, waypoints):
        try:
            directions_result = self.client.directions(
                origin=location,
                destination=location,
                waypoints=waypoints,
                mode="walking",
                optimize_waypoints=True,
            )
            if directions_result:
                insert_data(
                    {"timestamp": datetime.datetime.now(), "function": "directions"},
                    collection="statistics",
                )
                return directions_result[0]
            else:
                return {"message": "We could not generate directions"}

        except self.client.exceptions.ApiError as api_error:
            return {"error": "Google Maps API Error", "message": str(api_error)}

        except Exception as e:
            return {"error": "An unexpected error occurred", "message": str(e)}

    def check_workhours(self, place_id, date):
        try:
            place_details = self.get_place_details(place_id)
            opening_hours_data = (
                place_details["result"].get("opening_hours", {}).get("weekday_text", [])
            )
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            date_to_check = date_obj.date()
            day_of_week = date_to_check.weekday()
            if opening_hours_data:
                opening_hours_for_day = opening_hours_data[day_of_week]
                logger.info(opening_hours_for_day + place_details["result"]["name"])
                return "Closed" not in opening_hours_for_day
            else:
                logger.info("Opening hours data not available.")
                return False
        except Exception as e:
            logger.error("An unexpected error occurred:", e)
            return False

    def sort_places_by_working_hours(self, list_of_places, date):
        return [
            place
            for place in list_of_places
            if self.check_workhours(place.get("place_id"), date)
        ]

    def generate_raw_places(self, location, place_type):
        try:
            list_of_locations = self.get_places(location, place_type)
            return self.transform_places(list_of_locations)
        except Exception as e:
            print("An error occurred:", e)
            return []

    def generate_filtered_places(
        self, location, place_type, date, disable_workhours=False
    ):
        try:
            list_of_places = self.generate_raw_places(
                location=location, place_type=place_type
            )
            sorted_places = self.filter_places_by_rating(list_of_places)
            logger.info(f"Number of places that are filtered: {len(sorted_places)}")
            if disable_workhours:
                return sorted_places
            filtered_places = self.sort_places_by_working_hours(sorted_places, date)
            logger.info(f"Number of places to display: {len(filtered_places)}")
            if filtered_places:
                return filtered_places
            else:
                return []
        except Exception as e:
            return {"error": "An error occurred", "message": str(e)}

    @staticmethod
    def filter_places_by_rating(places):
        places = [
            place
            for place in places
            if place.get("rating") is not None
            and place.get("user_ratings_total", 0) > 10
        ]

        return places

    @staticmethod
    def filter_places_by_is_opened_status(list_of_places):
        return [place for place in list_of_places if place["is_opened"] is True]

    @staticmethod
    def create_waypoints(list_of_places):
        visits = [(place["lat"], place["lng"]) for place in list_of_places]
        return "|".join([f"{lat},{lng}" for lat, lng in visits])

    @staticmethod
    def transform_places(list_of_places):
        places = []
        try:
            for place in list_of_places:
                place_info = {
                    "business_status": place.get("business_status", "N/A"),
                    "is_opened": place.get("opening_hours", {}).get("open_now", "N/A"),
                    "lat": place["geometry"]["location"].get("lat", "N/A"),
                    "lng": place["geometry"]["location"].get("lng", "N/A"),
                    "name": place.get("name", "N/A"),
                    "user_ratings_total": place.get("user_ratings_total", 0),
                    "rating": place.get("rating", "N/A"),
                    "place_id": place.get("place_id"),
                    "place_type": place.get("types"),
                }
                places.append(place_info)
        except KeyError as key_error:
            logger.error(f"KeyError occurred: {key_error}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        logger.info(f"Number of all places: {len(places)}")
        return places
