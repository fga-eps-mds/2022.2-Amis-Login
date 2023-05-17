from fastapi import APIRouter, Depends, Form, HTTPException
from ...infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from src.application import social_worker_service

# Base.metadata.create_all(bind=engine)

router = APIRouter(
  prefix = '/login',
  tags = ['login'],
  responses = {404: {"description": "Not found"}},
)

socialWorkerRepository = SocialWorkerRepository()

@router.post("/")
async def login(username: str = Form(...), password: str = Form(...)):
    token = social_worker_service.login(socialWorkerRepository, username= username, password= password)
    return {
      "access_token": token,
      "token_type": "bearer",
    }

@router.get("/token")
async def verificarToken(token:str):
  return social_worker_service.verifyToken(token)