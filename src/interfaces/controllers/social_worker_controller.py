from database import get_db
from database import engine, Base
from sqlalchemy.orm import Session
from domain.models.social_worker import SocialWorkerResponse, SocialWorkerRequest
from domain.models.social_worker import SocialWorker, SocialWorkerDB
from domain.repositories.social_worker_repository import SocialWorkerRepository
# from domain.models.social_worker import SocialWorker
from security import get_password_hash
from fastapi import APIRouter, Depends, status, HTTPException, Response

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/socialWorker",
    tags=["socialWorker"]
)

# CREATE


@router.post("/",
             response_model=SocialWorkerResponse,
             status_code=status.HTTP_201_CREATED,)
def create(SocialWorker: SocialWorkerRequest, database: Session = Depends(get_db)):
    # TODO: Adicionar validação dos dados.
    assistentesModel = SocialWorkerDB(**SocialWorker.__dict__)
    assistentesModel.senha = get_password_hash(assistentesModel.senha)

    if SocialWorkerRepository.exists_by_login(database, assistentesModel.login):
        print("Já existe um login cadastrado")
        raise HTTPException(status_code=400, detail="login já cadastrado")

    assistentes = SocialWorkerRepository.save(
        database=database, SocialWorkerSent=assistentesModel)
    print(assistentes)
    return assistentes


# READ ALL
@router.get("/", response_model=list[SocialWorker])
def find_all(database: Session = Depends(get_db)):
    '''Faz uma query de todos os objetos assistente na DB (sem paginação)'''
    assistentes = SocialWorkerRepository.find_all(database)
    return [SocialWorkerResponse.from_orm(assistente) for assistente in assistentes]

# READ BY login


@router.get("/{login}", response_model=SocialWorker)
def find_by_login(login: str, database: Session = Depends(get_db)):
    '''Dado o login como parâmetro, encontra a assistente com esse login'''
    assistente = SocialWorkerRepository.find_by_login(database, login)
    if not assistente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    return SocialWorkerResponse.from_orm(assistente)

# UPDATE BY login


@router.put("/{login}", response_model=SocialWorker)
def update(request: SocialWorkerRequest, database: Session = Depends(get_db)):
    '''Dado o login da assistente, atualiza os dados cadastrais na DB por meio do método PUT'''
    login = request.login
    if not SocialWorkerRepository.exists_by_login(database, login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    assistente = SocialWorkerRepository.save(
        database, SocialWorkerDB(**request.dict()))
    return SocialWorkerResponse.from_orm(assistente)

# DELETE BY login


@router.delete("/{login}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_login(login: str, database: Session = Depends(get_db)):
    '''Dado o ID da assistente, deleta o objeto da DB por meio do método DELETE'''
    if not SocialWorkerRepository.exists_by_login(database, login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    SocialWorkerRepository.delete_by_login(database, login)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
