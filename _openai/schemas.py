from typing import Tuple

from graphene import String, ObjectType, ID, Int, Float, Date, Mutation
from graphene.types.argument import Argument
from graphene.types.field import Field
from graphene.types.scalars import Boolean
from datetime import datetime
from graphene.types.schema import Schema

from _openai.config import REQUEST_COUNT, get_model_by_id, add_model

class ModelType(ObjectType):
    _id= ID(required= True)
    disabled= Boolean(required= True)
    name= String(required= True)
    expires= Date(required= True)
    max_requests= Int(required=True)
    temperature= Float(default_value= 0.9)
    max_tokens= Int(default_value= 150)
    top_p= Float(default_value= 1.0)
    frequency_penalty= Float(default_value= 0.0)
    presence_penalty= Float(default_value= .6)
    best_of= Int(default_value= 1)


def data_validation(data: dict) -> Tuple[bool, str]:
    ...
    model_names = ['davinci', 'curie', 'babbage', 'ada',
        'davinci-instruct-beta', 'curie-instruct-beta'
    ]
    print(data)
    if data['name'] not in model_names:
        return False, 'The name of the model in invalid'
    elif not 0 <= data['temperature'] <= 1:
        return False, 'temperature must be in [0.0, 1.0]'
    elif not 0 < data['max_tokens'] <= 2048:
        return False, 'max_tokens must be (0, 2048]'
    elif not 0 <= data['top_p'] <= 1:
        return False, 'top_p must be [0, 1]'
    elif not 0 <= data['frequency_penalty'] <= 1:
        return False, 'frequency_penalty must be [0, 1]'
    elif not 0 <= data['presence_penalty'] <= 1:
        return False, 'presence_penalty must be [0, 1]'
    elif not 1 <= data['best_of'] <= 20:
        return False, 'top_p must be [1,20]'
    return True, ''

class CreateModel(Mutation):
    model = Field(ModelType)

    class Arguments:
        name= String(required= True)
        temperature= Float(default_value= 0.9)
        max_tokens= Int(default_value= 150)
        top_p= Float(default_value= 1.0)
        frequency_penalty= Float(default_value= 0.0)
        presence_penalty= Float(default_value= .6)
        best_of= Int(default_value= 1)
    
    async def mutate(self, info, **kwargs):
        data = kwargs
        data['max_requests'] = (REQUEST_COUNT * 64) // data['max_tokens']
        data['expires'] = datetime.today();
        data['disabled'] = True
        status, err = data_validation(data)
        if (status):
            data['_id'] = add_model(data).inserted_id
            return CreateModel(model= ModelType(**data))
        else:
            raise Exception(f"Error: Data validation checks failed ({err})")


class Query(ObjectType):
    model = Field(ModelType, _id= Argument(ID, required= True))

    async def resolve_model(self, info, _id):
        print(_id)
        return ModelType(**get_model_by_id(_id))


class Mutation(ObjectType):
    create_model = CreateModel.Field(required=True)

schema = Schema(query= Query, mutation=Mutation)