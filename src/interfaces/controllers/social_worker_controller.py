from database import get_db
from sqlalchemy.orm import Session
from domain.models.schema import SocialWorkerResponse, SocialWorkerRequest
from domain.models.social_worker import SocialWorker, SocialWorkerDB
from domain.repositories.social_worker_repository import SocialWorkerRepository
# from domain.models.social_worker import SocialWorker
from security import get_password_hash
from fastapi import APIRouter, Depends, status, HTTPException, Response

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

    if SocialWorkerRepository.exists_by_cpf(database, assistentesModel.cpf):
        print("Já existe um CPF cadastrado")
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

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

# READ BY CPF


@router.get("/{cpf}", response_model=SocialWorker)
def find_by_cpf(cpf: str, database: Session = Depends(get_db)):
    '''Dado o CPF como parâmetro, encontra a assistente com esse CPF'''
    assistente = SocialWorkerRepository.find_by_cpf(database, cpf)
    if not assistente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    return SocialWorkerResponse.from_orm(assistente)

# UPDATE BY CPF


@router.put("/{cpf}", response_model=SocialWorker)
def update(request: SocialWorkerRequest, database: Session = Depends(get_db)):
    '''Dado o CPF da assistente, atualiza os dados cadastrais na DB por meio do método PUT'''
    cpf = request.cpf
    if not SocialWorkerRepository.exists_by_cpf(database, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    assistente = SocialWorkerRepository.save(
        database, SocialWorkerDB(**request.dict()))
    return SocialWorkerResponse.from_orm(assistente)

# DELETE BY CPF


@router.delete("/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_cpf(cpf: str, database: Session = Depends(get_db)):
    '''Dado o ID da assistente, deleta o objeto da DB por meio do método DELETE'''
    if not SocialWorkerRepository.exists_by_cpf(database, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    SocialWorkerRepository.delete_by_cpf(database, cpf)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
