from datetime import datetime
from bson.objectid import ObjectId
from db import connect, get_model_by_id
from _openai.config import CLIENT_URI

def activate_model(model_id):
    if (cur := get_model_by_id(CLIENT_URI, 'openai', 'models')(model_id)) != {}:
        with connect(CLIENT_URI) as client:
            model = client['openai']['models']
            if cur.get('disabled'):
                result = model.update_one({'_id': ObjectId(model_id)}, {'$set': {'disabled': False, 'expires': datetime.fromordinal(datetime.today().toordinal() + 7)}})
            else:
                result = None
        return result
    return None




if __name__ == "__main__":
    activate_model('612a200cb878361e1c682bd9')