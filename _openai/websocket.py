from copy import error
from datetime import datetime
from typing import Literal, Optional, Union
from fastapi import WebSocket
from json import dumps
from pydantic import BaseModel
from starlette.authentication import requires

from _openai.config import get_model_by_id
from _openai.backend import call
import hashlib

class Message(BaseModel):
    model: str
    content: str
    hash_: str

class Content(BaseModel):
    code: int
    request: str
    response: str

class ErrorInfo(BaseModel):
    """
    ## Status Code
    These are the status code for each of the output condition
    #### status:success = 2xx
    #### status:error   = 3xx
    #### status:invalid = 4xx
    #### status:failure = 5xx
        
    """
    code: int
    request: str
    message: str 
    
class MessageResponse(BaseModel):
    status: Literal["success", "failure", "error", "invalid"]
    data: Optional[Content]
    error: Optional[ErrorInfo]

@requires(['authenticated'])
async def socketRoute(websocket: WebSocket):
    """
    Interaction with the socket

    """
    try:
        await websocket.accept()
        print((websocket.auth.scopes))
        while True:
            raw_data = await websocket.receive_json()


            data = Message(**raw_data)
            hash_ = data.hash_
            del raw_data['hash_']
            
            if hashlib.sha256(dumps(raw_data).encode()).hexdigest() != hash_:
                response = MessageResponse(
                    status= "invalid",
                    error= ErrorInfo(
                        code= 400,
                        request= data.json(),
                        message= "The hash check failed."
                    )
                )
                await websocket.send_json(response)
                return
            model = get_model_by_id(data.model)
            if model == {} or model.get('disabled') or model.get('expires') < datetime.today():
                response = MessageResponse(
                    status= "invalid",
                    error= ErrorInfo(
                        code= 400,
                        request= data.json(),
                        message= "The entered model ID is invalid, expired or disabled"
                    )
                )
                await websocket.send_json(response.dict())
                return
            output = MessageResponse(
                status= "success",
                data= Content(
                    code= 200,
                    request= data.json(),
                    response= dumps([i.to_dict() for i in call(data.model, data.content)['choices']])
                )
            )
            await websocket.send_json(output.dict())
            return
    except Exception as e:
        err_response = MessageResponse(
            status= "error",
            error= ErrorInfo(
                code= 300, # Depends on the Exception e
                request= '',
                message= f"{e}" # Depends on the Exception

            )
        )
        await websocket.send_json(err_response.dict())
        return
        
        

        



