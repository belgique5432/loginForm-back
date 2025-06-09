import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from dotenv import load_dotenv

load_dotenv()
client: AsyncIOMotorClient = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["belmulDataBase"]


def get_users_db() -> AsyncIOMotorCollection:
    return db["users"]