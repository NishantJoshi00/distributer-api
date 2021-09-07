from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser


class BaseAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return
        auth = request.headers["Authorization"]
        try:
            schema, token = auth.split(" ")
            if schema != 'Bearer':
                return
            print(token)    
            from _openai.config import ACCESS_TOKEN
            if token == ACCESS_TOKEN:
                return AuthCredentials(['authenticated']), SimpleUser('')
            # else:
                # return AuthCredentials(['authenticated'])
        except:
            return
