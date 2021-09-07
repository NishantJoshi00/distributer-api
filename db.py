from bson.objectid import ObjectId
from pymongo import MongoClient

def connect(DB_URI):
    client = MongoClient(DB_URI)
    return client

def get_model_by_id(DB_URI: str, db_name: str, collection_name: str):
    def inner_get_model_by_id(id):
        with connect(DB_URI) as client:
            model = client[db_name][collection_name]
            output = model.find_one({'_id': ObjectId(id)})
        return output or {}
    return inner_get_model_by_id

def add_model(DB_URI: str, db_name: str, collection_name: str):
    def inner_add_model(data):
        with connect(DB_URI) as client:
            db = client[db_name]
            model = db[collection_name]
            response = model.insert_one(data)
        return response
    return inner_add_model

