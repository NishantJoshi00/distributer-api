from fastapi import FastAPI

from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.middleware.authentication import AuthenticationMiddleware

from _openai.schemas import schema
from _openai.websocket import socketRoute

from security import BaseAuthBackend

app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend= BaseAuthBackend())

app.add_route("/gql", GraphQLApp(schema= schema, executor_class= AsyncioExecutor))
app.add_websocket_route("/connect", route= socketRoute)

