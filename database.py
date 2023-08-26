from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from bson.errors import InvalidId
from helpers import locations_helper

mongodb_uri = os.environ.get("MONGODB_URL")
client = MongoClient(mongodb_uri)
db = client["map_dev"]
locations_collection = db["locations"]


def insert_data(data_set, collection):
    try:
       collection = db[collection]
       new_data = collection.insert_one(data_set).inserted_id
       return str(new_data)
    except Exception as e:
        print(f"error has occurred:{e}")
        return None


def get_data(data_id, collection):
    try:
        collection = db[collection]
        locations_data_set = collection.find_one({"_id": ObjectId(data_id)})
        if collection == locations_collection:
            return locations_helper(locations_data_set)
    except Exception as e:
        print(f"error as occured:{e}")
        return None