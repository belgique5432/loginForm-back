from typing import Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel, Field, field_validator
from database.db import get_users_db
import re

users_db: AsyncIOMotorCollection = get_users_db()

class User(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    user_name: str
    password: str

    @field_validator('password')
    def password_validation(cls, value: str) -> str:
        """
        Valida la contraseña:
            - No debe contener espacios.
            - Debe tener al menos 8 caracteres.
            - Debe incluir al menos una letra mayúscula.
            - Debe contener al menos un número.
            - Debe tener al menos un carácter especial.
        """
        if ' ' in value:
            raise ValueError('Password cannot contain spaces')
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least 1 uppercase character')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least 1 number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Password must contain at least 1 special character')
        return value