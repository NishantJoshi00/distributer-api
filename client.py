# import requests
# from requests.auth import AuthBase


# class BearerAuth(AuthBase):
#     def __init__(self, token):
#         self.token = token
    
#     def __call__(self, r):
#         r.headers['authorization'] = "Bearer " + self.token
#         return r
    

# query = """
# query {
#     user
# }
# """

# d = requests.post('http://localhost:8000/gql', json= {'query': query}, auth= BearerAuth("glkL;GgdahGTJA"))

# print(d.json())

# import json, hashlib

# with open('test.json') as f:
#     data = json.load(f)
#     del data['hash_']

# data['hash_'] = hashlib.sha256(json.dumps(data).encode()).hexdigest()
# with open("test.json", 'w') as f:
#     json.dump(data, f)

# from _openai.authorizer import activate_model

# activate_model('61365a19a1f410e555185dfd')

# from _openai.backend import call



# call("61365a19a1f410e555185dfd", "hello")