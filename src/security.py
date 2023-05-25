import os
from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
authSchema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = os.getenv('SECRET_KEY', 'amis2023')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS512')
ALGORITHM="HS512"
ACCESS_TOKEN_EXPIRE_HOURS=1
REFRESH_TOKEN_EXPIRE_HOURS=2

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
