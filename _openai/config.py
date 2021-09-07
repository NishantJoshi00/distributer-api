from pymongo import results
from db import get_model_by_id, add_model, connect
import os, json
ENV = 'json'
OPERATIONAL_PERIOD, REQUEST_COUNT = 7, 10
if ENV == 'env':
    API_KEY, CLIENT_URI, ACCESS_TOKEN = os.getenv("API_KEY"), os.getenv("CLIENT_URI"), os.getenv("ACCESS_TOKEN")
    DATABASE, COLLECTION = os.getenv("DATABASE"), os.getenv("COLLECTION")
elif ENV == 'json':
    with open('_openai/config.json') as f:
        data = json.load(f)
        API_KEY, CLIENT_URI, ACCESS_TOKEN = data.get("API_KEY"), data.get("CLIENT_URI"), data.get("ACCESS_TOKEN")
        DATABASE, COLLECTION = data.get("DATABASE"), data.get("COLLECTION")
        

get_model_by_id = get_model_by_id(CLIENT_URI, DATABASE, COLLECTION)
add_model = add_model(CLIENT_URI, DATABASE, COLLECTION)

def debit_request_from_model(model_id, change=-1):
    if (cur := get_model_by_id(CLIENT_URI, DATABASE, COLLECTION)) != {}:
        if cur.get('max_requests') <= 0:
            return -1, None
        else:
            with connect(CLIENT_URI) as client:
                model = client['openai']['models']
                results = model.update_one({'_id': model_id}, {'$set': {'max_requests': cur.get('max_requests') + change}})
            return 0, results
    else:
        return 1, None
