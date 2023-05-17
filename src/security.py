import os
import json
from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from .infrastructure.repositories.social_worker_repository import AssistentesRepository
from sqlalchemy.orm import Session
from .database import engine, Base, get_db as get_database
from .domain.models.social_worker import Assistentes

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
authSchema = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = os.getenv('SECRET_KEY', 'amis2023')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS512')
ALGORITHM="HS512"
ACCESS_TOKEN_EXPIRE_HOURS = 1

def criar_token_jwt(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verificar_token(token: str) -> Assistentes:
    decoded_jwt = jwt.decode(token, SECRET_KEY, ALGORITHM).get('sub')

    return decoded_jwt

def obter_usuario_logado(database: Session = Depends(get_database), token: str = Depends(authSchema)) -> bool:
    try:
        assistente = verificar_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = {"response": "Token inválido", "status_code": status.HTTP_401_UNAUTHORIZED})

    if not assistente:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = {"response": "Token inválido", "status_code": status.HTTP_401_UNAUTHORIZED})

    
    assistenteReturn = AssistentesRepository.find_by_login(database, assistente)

    if not assistenteReturn:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = {"response": "Token inválido", "status_code": status.HTTP_401_UNAUTHORIZED})

    assistenteReturn.senha = None

    return assistenteReturn
