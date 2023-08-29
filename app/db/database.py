from pymongo import MongoClient
import os

mongodb_uri = os.environ.get("MONGODB_URL")
client = MongoClient(mongodb_uri)
db = client["map_dev"]

