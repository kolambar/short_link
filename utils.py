from random import choice
from motor.motor_asyncio import AsyncIOMotorClient


def create_short_link(conection_to_mongo: AsyncIOMotorClient, link: str) -> str:
    """
    Генерирует короткую ссылку
    :param conection_to_mongo:
    :param link:
    :return short_link:
    """
    # Список возможных символов
    symbols = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # Сгенерировать случайную последовательность из 6 символов списка
    short_link = "".join([choice(symbols) for _ in range(6)])

    return short_link
