from pymongo import MongoClient
import os

mongodb_uri = os.environ.get("MONGO_DB_URL")
client = MongoClient(mongodb_uri)
db = client["map_dev"]
