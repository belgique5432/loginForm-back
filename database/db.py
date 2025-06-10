import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

MONGO_URI = os.getenv("MYAPP_MONGO_URI")
if not MONGO_URI:
    raise ValueError("La variable de entorno MYAPP_MONGO_URI no está definida")

client = AsyncIOMotorClient(MONGO_URI)
db = client["belgi"]

print("MONGO_URI =", MONGO_URI)
print("CLIENT:", client)

def get_users_db() -> AsyncIOMotorCollection:
    return db["users"]
