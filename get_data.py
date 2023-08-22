import googlemaps
import os
from datetime import datetime
import csv
import uuid


api_key = os.environ.get('MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)

tags_dict = {"religious_tourism":["church","sinagoge","hindu_temple", "tourist_attraction", "mosque"],
             "animal_sighting":["zoo","aquarium"]}

def convert_location_to_geocode(location):
    result = gmaps.geocode(location)
    return result[0]['geometry']['location']

def write_data_to_csv(data_list):
    output_file = f'{str(uuid.uuid4())}.csv'
    if not data_list:
        print("Data list is empty. Nothing to write to CSV.")
        return
    field_names = data_list[0].keys()
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for row in data_list:
            writer.writerow(row)

    print(f"Data successfully written to {output_file}")
    return output_file[:-4]


def get_places(location, place_type):
    geocoded_location = convert_location_to_geocode(location)
    places_raw = gmaps.places_nearby(location=geocoded_location, type=place_type, radius=5000)
    places_unfiltered = places_raw['results']
    places = []
    for place in places_unfiltered:
        place_info = {
                "business_status" : place.get("business_status", "N/A"),
                "is_opened": place.get("opening_hours",{}).get("open_now", "N/A"),
                "lat": place["geometry"]["location"].get("lat","N/A"),
                "lng": place["geometry"]["location"].get("lng","N/A"),
                "name": place.get("name"),
                "user_ratings_total" : place.get("user_ratings_total","N/A"),
                "rating": place.get("rating"),
                "place_id": place.get("place_id"),
                "place_type": place.get("place_type")
             }
        places.append(place_info)
    print(f"number of all places {len(places)}")
    return places

def get_working_hours(place_id, date):
    place_details = gmaps.place(place_id)
    opening_hours_data = place_details["result"].get("opening_hours", {}).get("weekday_text", [])
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_to_check = datetime.date(date_obj)
    day_of_week = date_to_check.weekday()

    if opening_hours_data:
        opening_hours_for_day = opening_hours_data[day_of_week]
        print(opening_hours_for_day + place_details["result"]["name"])
        return "Closed" not in opening_hours_for_day
    else:
        return False


def get_directions(location, place_type, date):
    list_of_places = get_places(location, place_type)
    places_temp = [
        place
        for place in list_of_places
        if place['business_status'] == 'OPERATIONAL'
        and place['rating'] is not None
        and place['user_ratings_total'] > 10
    ]
    print(f"number of places that are filtered {len(places_temp)}")
    filtered_places = [
        place for place in places_temp if get_working_hours(place['place_id'], date)
    ]
    print(f"number of places to display {len(filtered_places)}")
    name_of_csv = {"csv_id":write_data_to_csv(filtered_places)}
    visits = [(place["lat"], place["lng"]) for place in filtered_places]
    waypoints = "|".join([f"{lat},{lng}" for lat, lng in visits])
    if directions_result := gmaps.directions(
        origin=location,
        destination=location,
        waypoints=waypoints,
        mode="walking",
        optimize_waypoints=True,
    ):
        return [filtered_places,directions_result[0], name_of_csv]
    else:
        return None