from app.db.database import db
from bson.objectid import ObjectId


def insert_data(data_set, collection):
    try:
        collection = db[collection]
        print(data_set)
        new_data = collection.insert_one(data_set).inserted_id
        return str(new_data)
    except Exception as e:
        print(f"error has occurred:{e}")
        return None


def get_data(data_id, collection):
    try:
        collection = db[collection]
        locations_data_set = collection.find_one({"_id": ObjectId(data_id)})
        return locations_data_set
    except Exception as e:
        print(f"error has occurred:{e}")
        return None


def get_specific_field_by_foreign_key(foreign_key, field_name, collection):
    try:
        collection = db[collection]
        pipeline = [
            {"$match": {"location_reference": ObjectId(foreign_key)}},
            {"$project": {field_name: 1, "_id": 0}},
        ]

        result = list(collection.aggregate(pipeline))
        return result

    except Exception as error:
        print("An error occurred:", error)
        return []
