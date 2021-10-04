from typing import List

import graphene
import uvicorn
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from model.models_hw3 import User, WordUnit

users: List[User] = [
    User(88, "supergirl88", [WordUnit("cat", "кот", 10, 9)]),
    User(5, "Dream", [WordUnit("mask", "маска", 5, 5)]),
    User(404, "NotFound", [WordUnit("error", "ошибка", 15, 0)])
]


class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.Int())

    def resolve_user(self, info, id):
        for user in users:
            if user.id == id:
                return user
        return None


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
