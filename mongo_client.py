from motor.motor_asyncio import AsyncIOMotorClient
from envparse import Env


env = Env()
#  Настройки подключения к бд
MONGODB_URL = env.str("MONGODB_URL", default="localhost:27017")

#  Создает клиента для MongoDB
client = AsyncIOMotorClient(MONGODB_URL)
