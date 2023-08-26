from datetime import datetime
import os
import uuid
from pydantic import ValidationError
import csv
import json
from get_data import get_place_details


def write_data_to_csv(data_list):
    try:
        output_directory = "csv"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        file_name = f"{str(uuid.uuid4())}.csv"
        output_file = os.path.join(output_directory, file_name)
        if not data_list:
            print("Data list is empty. Nothing to write to CSV.")
            return None

        field_names = data_list[0].keys()
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)

            writer.writeheader()

            for row in data_list:
                writer.writerow(row)

        print(f"Data successfully written to {file_name}")
        return file_name[:-4]
    except Exception as e:
        print("An error occurred:", e)
        return None


def check_workhours(place_id, date):
    try:
        place_details = get_place_details(place_id)
        opening_hours_data = (
            place_details["result"].get("opening_hours", {}).get("weekday_text", [])
        )
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
    except Exception as e:
        print("An unexpected error occurred:", e)
        return False


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
        print(f"KeyError occurred: {key_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"Number of all places: {len(places)}")
    return places


def locations_helper(locations_data) -> dict:
    try:
        extracted_locations = []
        for location in locations_data["locations"]:
            location = {
                "name": location.get("name", "N/A"),
                "lat": location.get("lat", 0.0),
                "lng": location.get("lng", 0.0),
                "rating": location.get("rating", 0.0),
                "place_type": location.get("place_type", "N/A"),
                "user_ratings_total": location.get("user_ratings_total", 0),
            }
            extracted_locations.append(location)

        return {
            "id": str(locations_data.get("_id", "")),
            "date": locations_data.get("date", "N/A"),
            "start_location": locations_data.get("start_location", "N/A"),
            "locations": extracted_locations,
        }

    except KeyError as key_error:
        return {"KeyError": f"Key '{key_error.args[0]}' not found in locations_data"}

    except Exception as e:
        print(f"An error occurred: {e}")

def validate_json_response(json_response, pydantic_model):
    try:
        parsed_json = json.loads(json_response)
        validated_data = pydantic_model(**parsed_json)
        return True, validated_data
    except json.JSONDecodeError:
        return False, "Invalid JSON response"
    except ValidationError as e:
        return False, e.errors()
