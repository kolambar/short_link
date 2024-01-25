from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from fastapi import FastAPI

from mongo_client import client


app = FastAPI()
app.state.mongo_client = client

