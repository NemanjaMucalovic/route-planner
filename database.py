from pymongo import MongoClient
from bson.objectid import ObjectId

mongodb_uri = "mongodb://localhost:27017"
client = MongoClient(mongodb_uri)
db = client['map_dev']
directions_collection = db['directions']
locations_collection = db['locations']

def insert_data(data_set, collection):
     collection = db[collection]
     new_locations = collection.insert_one(data_set).inserted_id
     return str(new_locations)

def get_data(data_id, collection):
     collection = db[collection]
     locations_data_set = collection.find_one({"_id": ObjectId(data_id)})
     if collection == locations_collection:
         return locations_helper(locations_data_set)


def locations_helper(locations_data) -> dict:
    extracted_locations = []
    for location in locations_data["locations"]:
        location = {
            "name": location["name"],
            "lat": location["lat"],
            "lng": location["lng"],
            "rating": location["rating"],
            "place_type": location["place_type"],
            "user_ratings_total": location["user_ratings_total"]
        }
        extracted_locations.append(location)
    return {
        "id": str(locations_data["_id"]),
        "date": locations_data["date"],
        "start_location": locations_data["start_location"],
        "locations": extracted_locations
    }

