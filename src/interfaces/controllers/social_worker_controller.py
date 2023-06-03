from database import get_db
from database import engine, Base
from sqlalchemy.orm import Session
from domain.models.social_worker import SocialWorkerResponse, SocialWorkerRequest
from domain.models.social_worker import SocialWorker, SocialWorkerDB
from security import get_password_hash
from fastapi import APIRouter, Depends, status, HTTPException, Response

from interfaces.controllers import socialWorkersService

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/socialWorker",
    tags=["socialWorker"]
)


# CREATE

@router.post("/", status_code=status.HTTP_201_CREATED,)
def create(social_worker_request: SocialWorkerRequest, database: Session = Depends(get_db)):
    fieldsValidation = socialWorkersService.validate_social_worker(
        social_worker_request
    )

    if not fieldsValidation['completeStatus']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)

    social_worker_model = SocialWorkerDB(**social_worker_request.__dict__)
    social_worker_model.senha = get_password_hash(social_worker_model.senha)

    if socialWorkersService.exists_by_login(social_worker_model.login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="login já cadastrado")

    socialWorkersService.save(socialWorkerSent=social_worker_model)

    return social_worker_request


# READ ALL

@router.get("/", response_model=list[SocialWorker])
def find_all():
    '''Faz uma query de todos os objetos assistente na DB (sem paginação)'''
    social_workersDB = socialWorkersService.find_all()
    return social_workersDB

# READ BY login


@router.get("/{login}", response_model=SocialWorker)
def find_by_login(login: str) -> SocialWorkerResponse:
    """Dado o login da assistente, retorna o objeto da assistente"""
    social_worker = socialWorkersService.find_by_login(login)
    if not social_worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    return SocialWorkerResponse.from_orm(social_worker)

# UPDATE BY login


@router.put("/{login}", response_model=SocialWorker)
def update(request: SocialWorkerRequest):
    '''Dado o login da assistente, atualiza os dados cadastrais na DB por meio do método PUT'''
    fieldsValidation = socialWorkersService.validate_social_worker(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)

    login = request.login
    if not socialWorkersService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    assistente = socialWorkersService.save(SocialWorkerDB(**request.dict()))
    return SocialWorkerResponse.from_orm(assistente)

# DELETE BY login


@router.delete("/{login}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_login(login: str):
    '''Dado o ID da assistente, deleta o objeto da DB por meio do método DELETE'''

    if not socialWorkersService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    socialWorkersService.delete_by_login(login)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
