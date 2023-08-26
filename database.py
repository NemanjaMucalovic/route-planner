from pymongo import MongoClient
from bson.objectid import ObjectId
from helpers import locations_helper

mongodb_uri = "mongodb://localhost:27017"
client = MongoClient(mongodb_uri)
db = client['map_dev']
locations_collection = db['locations']

def insert_data(data_set, collection):
     collection = db[collection]
     new_data = collection.insert_one(data_set).inserted_id
     return str(new_data)

def get_data(data_id, collection):
     collection = db[collection]
     locations_data_set = collection.find_one({"_id": ObjectId(data_id)})
     if collection == locations_collection:
         return locations_helper(locations_data_set)


