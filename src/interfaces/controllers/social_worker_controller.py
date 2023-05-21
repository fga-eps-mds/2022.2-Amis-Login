from database import get_db
from sqlalchemy.orm import Session
from domain.schemas.socialWorker import SocialWorker, SocialWorkerResponse, SocialWorkerResponse
from domain.repositories.social_worker_repository import SocialWorkerRepositoryBaseModel as SocialWorkerRepository
from domain.models.social_worker import SocialWorker
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
def create(socialWorker: SocialWorkerResponse, database: Session = Depends(get_db)):
    # TODO: Adicionar validação dos dados.
    socialWorkerModel = SocialWorker(**socialWorker.dict())
    socialWorkerModel.senha = get_password_hash(socialWorkerModel.senha)

    if SocialWorkerRepository.exists_by_cpf(database, socialWorkerModel.cpf):
        print("Já existe um CPF cadastrado")
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    SocialWorker = SocialWorkerRepository.save(
        database=database, SocialWorker=socialWorkerModel)
    print(SocialWorker)
    return SocialWorker


# READ ALL 
@router.get("/", response_model=list[SocialWorker])
def find_all(database: Session = Depends(get_db)):
    '''Faz uma query de todos os objetos socialWorker na DB (sem paginação)'''
    SocialWorker = SocialWorkerRepository.find_all(database)
    return [SocialWorkerResponse.from_orm(socialWorker) for socialWorker in SocialWorker]

# READ BY CPF
@router.get("/{cpf}", response_model=SocialWorker)
def find_by_cpf(cpf: str, database: Session = Depends(get_db)):
    '''Dado o CPF como parâmetro, encontra a socialWorker com esse CPF'''
    socialWorker = SocialWorkerRepository.find_by_cpf(database, cpf)
    if not socialWorker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="socialWorker não encontrada"
        )
    return SocialWorkerResponse.from_orm(socialWorker)

# UPDATE BY CPF
@router.put("/{cpf}", response_model=SocialWorker)
def update(request: SocialWorkerResponse, database: Session = Depends(get_db)):
    '''Dado o CPF da socialWorker, atualiza os dados cadastrais na DB por meio do método PUT'''
    cpf = request.cpf
    if not SocialWorkerRepository.exists_by_cpf(database, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="socialWorker não encontrada"
        )
    socialWorker = SocialWorkerRepository.save(
        database, SocialWorker(**request.dict()))
    return SocialWorkerResponse.from_orm(socialWorker)

# DELETE BY CPF
@router.delete("/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_cpf(cpf: str, database: Session = Depends(get_db)):
    '''Dado o ID da socialWorker, deleta o objeto da DB por meio do método DELETE'''
    if not SocialWorkerRepository.exists_by_cpf(database, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="socialWorker não encontrada"
        )
    SocialWorkerRepository.delete_by_cpf(database, cpf)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
