from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from fastapi import FastAPI

from mongo_client import client
from utils import create_short_link


app = FastAPI()
app.state.mongo_client = client

@app.post("/short_link/", response_model=str)
async def create_secret(link: dict, request: Request) -> str:
    conection_to_mongo: AsyncIOMotorClient = request.app.state.mongo_client["short_link_bd"]
    short_link = create_short_link(conection_to_mongo, link['link'])
    return short_link
