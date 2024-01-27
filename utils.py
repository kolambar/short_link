import json
from random import choice
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Response, status
from settings import symbols, domain, logging


def create_short_link() -> str:
    """
    Генерирует короткую ссылку
    :return short_link:
    """
    # Сгенерировать случайную последовательность из 6 символов списка
    short_link = "".join([choice(symbols) for _ in range(6)])

    return short_link


async def record_link(connection_to_mongo: AsyncIOMotorClient, link: str) -> Response:
    """
    Записывает в базу данных короткую ссылку и возвращает ее пользователю
    :param connection_to_mongo:
    :param link:
    :return:
    """

    logging.info(f"Начало записи ссылки: {link}")

    # Проверка на существование этой ссылки в бд
    same_link_from_db = await connection_to_mongo.records.find_one({"link": link})
    if not same_link_from_db:  # Если нет, то генерируем новую
        short_link = create_short_link()
        # Если новая короткая ссылка совпадает с какой-то уже существующей, перезаписываем только что созданную
        while await connection_to_mongo.records.find_one({"short_link": short_link}):
            short_link = create_short_link()
            logging.info(f"Генерация новой короткой ссылки из-за коллизии: {short_link}")

        # Записываем новую короткую ссылку и ссылку от пользователя в бд
        connection_to_mongo.records.insert_one({"short_link": short_link, "link": link})
        logging.info(f"Короткая ссылка {short_link} успешно записана в базу данных и отдана пользователю")

        # Создаем объект Response
        response = Response(
            status_code=status.HTTP_201_CREATED,
            content=json.dumps({"short_link": f'{domain}go/{short_link}'})
        )
        # Логируем код ответа
        logging.info(f"Код ответа: {response.status_code}")
        return response
    else:  # Если ссылка существует в бд, то возвращаем ее короткую ссылку
        logging.info(f"Ссылка {link} уже существует в базе данных. Возвращаем короткую ссылку: "
                     f"{same_link_from_db['short_link']}")

        # Создаем объект Response
        response = Response(
            status_code=status.HTTP_200_OK,
            content=json.dumps({"short_link": f'{domain}go/{same_link_from_db["short_link"]}'})
        )
        # Логируем код ответа
        logging.info(f"Код ответа: {response.status_code}")
        return response
