import datetime

from pymongo.errors import ServerSelectionTimeoutError

from settings import logging
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse

from mongo_client import client
from utils import record_link, get_short_code


app = FastAPI()
app.state.mongo_client = client


@app.post("/short_link/")
async def create_short_link(link: dict, request: Request) -> Response:
    # Логируем запрос
    logging.info(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Запрос на создание короткой ссылки получен от клиента с IP-адресом {request.client.host}, "
        f"метод запроса: {request.method}, "
        f"запрашиваемый путь: {request.url}"
    )
    # Получаем ссылку
    link = link['link']
    try:
        connection_to_mongo: AsyncIOMotorClient = request.app.state.mongo_client["short_link_bd"]  # подключение к бд
        response = await record_link(connection_to_mongo, link)

        return response
    except ServerSelectionTimeoutError as e:
        # Логируем ошибку
        logging.error(f"Ошибка подключения к базе данных: {e}")
        # Возвращаем ответ с кодом состояния 500
        return Response(status_code=500, content='Не удалось подключиться к базе данных')


@app.get("/go/{short_link}")
async def go_to_short_link(short_link: str, request: Request):
    # Логируем запрос
    logging.info(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Запрос на переход по короткой ссылки получен от клиента с IP-адресом {request.client.host}, "
        f"метод запроса: {request.method}, "
        f"запрашиваемый путь: {request.url}"
    )
    try:
        connection_to_mongo: AsyncIOMotorClient = request.app.state.mongo_client["short_link_bd"]  # подключение к бд

        # Получаем из бд нужную ссылку и редиректим на нее
        necessary_dict = await connection_to_mongo.records.find_one({"short_link": short_link})
        if not necessary_dict:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        link = necessary_dict['link']

        # Создаем объект Response
        response = RedirectResponse(link, status_code=301)
        # Логируем код ответа
        logging.info(f"Код ответа: {response.status_code}")

        return response
    except ServerSelectionTimeoutError as e:
        # Логируем ошибку
        logging.error(f"Ошибка подключения к базе данных: {e}")
        # Возвращаем ответ с кодом состояния 500
        return Response(status_code=500, content='Не удалось подключиться к базе данных')


@app.delete("/del/")
async def delete_short_link(short_link: dict, request: Request) -> Response:
    # Логируем запрос
    logging.info(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Запрос на удаление по короткой ссылки получен от клиента с IP-адресом {request.client.host}, "
        f"метод запроса: {request.method}, "
        f"запрашиваемый путь: {request.url}"
    )
    try:
        connection_to_mongo: AsyncIOMotorClient = request.app.state.mongo_client["short_link_bd"]  # подключение к бд
        short_code = get_short_code(short_link)
        if await connection_to_mongo.records.find_one({"short_link": short_code}):
            # Удаляем из бд нужную ссылку
            connection_to_mongo.records.delete_one({"short_link": short_code})
            # Создаем объект Response
            response = Response(status_code=200, content='Данные с этой короткой ссылкой удалены')
            # Логируем код ответа
            logging.info(f"Код ответа: {response.status_code}")
            return response
        else:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
    except ServerSelectionTimeoutError as e:
        # Логируем ошибку
        logging.error(f"Ошибка подключения к базе данных: {e}")
        # Возвращаем ответ с кодом состояния 500
        return Response(status_code=500, content='Не удалось подключиться к базе данных')
