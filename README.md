# OPENAI GPT-3 API DISTRIBUTER
- This is my personal project implementing the openAI GPT-3 text completion models, to serve API calls to other applications & websites through websocket & graphQL.
- Creating an abstracting between the client application and the main query runner, limiting the requests and adding admin authorization and model based access

## Implementation
This API is built fully on `FastAPI`
- Install all the modules given in the requirements.txt file
- run `python3 -m uvicorn main:app`
- Done! Check the localhost:8000/gql to get started
- The websocket can be accessed at localhost:8000/connect