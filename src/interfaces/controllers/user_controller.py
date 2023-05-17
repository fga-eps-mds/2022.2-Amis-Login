from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Form, HTTPException
from ...database import engine, Base, get_db as get_database
from ...domain.models.social_worker import Assistentes as Assistente
from ...security import criar_token_jwt, verify_password, obter_usuario_logado
from ...infrastructure.repositories.social_worker_repository import AssistentesRepository

Base.metadata.create_all(bind=engine)

router = APIRouter(
  prefix = '/login',
  tags = ['login'],
  responses = {404: {"description": "Not found"}},
)

@router.post("/")
async def login(username: str = Form(...), password: str = Form(...)):
    assistente = AssistentesRepository.find_by_login(database, login=username)
    if not assistente or not verify_password(password, assistente.senha):
        raise HTTPException(
          status_code=403,
          detail="Email ou nome de usuário incorretos"
        )
    return {
      "access_token": criar_token_jwt(assistente.login),
      "token_type": "bearer",
    }

@router.get("/token")
async def verificarToken(usuario: Assistente = Depends(obter_usuario_logado)):
  return usuario