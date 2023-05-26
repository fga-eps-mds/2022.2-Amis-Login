from fastapi import APIRouter, Form, Header, HTTPException
from infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from infrastructure.repositories.tokens_repository import TokensRepository
from application.social_worker_service import SocialWorkerService
from infrastructure.repositories.tokens_repository import TokensRepository

from fastapi import APIRouter, Form, Header, HTTPException, status

from interfaces.controllers import socialWorkersService

router = APIRouter(
    prefix='/login',
    tags=['login'],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def login(username: str = Form(...), password: str = Form(...)):
    access_token, refresh_token = socialWorkersService.login(
        username=username, password=password)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/token", status_code=201)
async def verificarToken(authorization: str = Header(...)):
    socialWorker = socialWorkersService.verifyToken(authorization)
    socialWorker.senha = None
    return socialWorker


@router.post("/token/refresh", status_code=201)
async def refreshToken(refresh_token: str = Header(...)):
    tokens = socialWorkersService.refreshSession(refresh_token=refresh_token)
    if tokens:
        return {
            "access_token": tokens[0],
            "refresh_token": tokens[1],
            "token_type": "bearer",
        }

    raise HTTPException(401, "Not Allowed")


@router.post("/logout")
def logout(refresh_token: str = Header(...)):
    socialWorkersService.delete_refresh_token(refresh_token)

    return {"message": "Logout realizado com sucesso"}
