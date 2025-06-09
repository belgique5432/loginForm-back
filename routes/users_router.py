from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from motor.motor_asyncio import AsyncIOMotorCollection
from database.db import get_users_db
from passlib.hash import bcrypt
from models.users import User

users_router = APIRouter()

SECRET_KEY = "password"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@users_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_db: AsyncIOMotorCollection = Depends(get_users_db)
):
    username = form_data.username
    password = form_data.password

    user = await users_db.find_one({"user_name": username})

    if not user or not bcrypt.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Wrong password or username")

    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


@users_router.post("/create_user")
async def create_user(
    user: User,
    users_db: AsyncIOMotorCollection = Depends(get_users_db) 
):
    existing_user = await users_db.find_one({"user_name": user.user_name})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = bcrypt.hash(user.password)
# 

    new_user = {
        "user_name": user.user_name,
        "password": hashed_password,
    }

    result = await users_db.insert_one(new_user)

    return {
        "id": str(result.inserted_id),
        "user_name": user.user_name,
    }
