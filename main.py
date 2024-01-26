from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

from mongo_client import client
from utils import record_link


app = FastAPI()
app.state.mongo_client = client


@app.post("/short_link/")
async def create_secret(link: dict, request: Request) -> Response:
    link = link['link']

    connection_to_mongo: AsyncIOMotorClient = request.app.state.mongo_client["short_link_bd"]  # подключение к бд
    response = await record_link(connection_to_mongo, link)

    return response


@app.get("/go/{short_link}")
async def go_to_short_link(short_link: str, request: Request):
    connection_to_mongo: AsyncIOMotorClient = request.app.state.mongo_client["short_link_bd"]  # подключение к бд

    # Получаем из бд нужную ссылку и редиректим на нее
    necessary_dict = await connection_to_mongo.records.find_one({"short_link": short_link})
    link = necessary_dict['link']
    return RedirectResponse(link, status_code=301)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
