from ..domain.repositories.social_worker_repository import SocialWorkerRepositoryBaseModel
from src.security import criar_token_jwt, verify_password, verificar_token
from src.domain.models.social_worker import SocialWorker
from fastapi import HTTPException
from typing import Type

def login(usersRepository: Type[SocialWorkerRepositoryBaseModel], username: str , password: str ) -> str:
  socialWorker = usersRepository.find_by_login(username)
  if not socialWorker or not verify_password(password, socialWorker.senha):
    raise HTTPException(
      status_code=403,
      detail="Email ou nome de usuário incorretos"
    )
  
  return criar_token_jwt(socialWorker.login)

def verifyToken (usersRepository: Type[SocialWorkerRepositoryBaseModel], token:str ) -> SocialWorker:
  userLogin = verificar_token(token= token)
  socialWorker = usersRepository.find_by_login(userLogin)

  return socialWorker