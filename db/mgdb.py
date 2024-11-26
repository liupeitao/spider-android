from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request


def get_mongo(requests: Request) -> AsyncIOMotorClient:
    return requests.app.state.mongo
